"""
Motor de áudio para a MelodyScript.
Responsável pela síntese e reprodução de notas musicais.
"""

import threading
import time

import numpy as np
import pygame


class AudioEngine:
    """Motor de áudio para reprodução de notas musicais."""

    # Definição dos perfis de instrumentos com suas características
    PERFIS_INSTRUMENTOS = {
        "piano": {
            "waveform": "sine",
            "attack": 0.01,
            "decay": 0.1,
            "sustain": 0.7,
            "release": 0.3,
            "harmonic_profile": [(1.0, 1.0), (0.7, 2.0), (0.4, 3.0), (0.25, 4.0)],
            "description": "Som clássico de piano com decay natural",
        },
        "guitarra": {
            "waveform": "sawtooth",
            "attack": 0.005,
            "decay": 0.15,
            "sustain": 0.5,
            "release": 0.1,
            "harmonic_profile": [(1.0, 1.0), (0.85, 2.0), (0.6, 3.0), (0.5, 4.0), (0.4, 5.0), (0.3, 6.0)],
            "description": "Timbre brilhante de guitarra elétrica",
        },
        "violino": {
            "waveform": "sine",
            "attack": 0.15,
            "decay": 0.05,
            "sustain": 0.9,
            "release": 0.3,
            "harmonic_profile": [(1.0, 1.0), (0.5, 2.0), (0.35, 3.0), (0.15, 4.0), (0.1, 5.0)],
            "description": "Som suave e expressivo de violino",
        },
        "flauta": {
            "waveform": "sine",
            "attack": 0.08,
            "decay": 0.03,
            "sustain": 0.95,
            "release": 0.1,
            "harmonic_profile": [(1.0, 1.0), (0.1, 2.0), (0.05, 3.0)],
            "description": "Som puro e delicado de flauta",
        },
        "baixo": {
            "waveform": "triangle",
            "attack": 0.04,
            "decay": 0.2,
            "sustain": 0.8,
            "release": 0.3,
            "harmonic_profile": [(1.0, 1.0), (0.6, 2.0), (0.3, 3.0), (0.2, 4.0), (0.1, 5.0)],
            "description": "Som profundo e ressoante de baixo",
        },
        "sintetizador": {
            "waveform": "square",
            "attack": 0.01,
            "decay": 0.0,
            "sustain": 1.0,
            "release": 0.05,
            "harmonic_profile": [(1.0, 1.0), (0.1, 3.0), (0.3, 5.0), (0.2, 7.0)],
            "description": "Som sintético quadrado com característica eletrônica",
        },
    }

    def __init__(self):
        """Inicializa o motor de áudio."""
        pygame.mixer.init(44100, -16, 2, 512)
        self.sample_rate = 44100

        # Instrumento atual (padrão: piano)
        self.instrumento_atual = "piano"

        # Carrega as configurações do instrumento padrão
        self._carregar_perfil_instrumento(self.instrumento_atual)

        # Lista para rastrear sons ativos
        self.active_sounds = []
        self.sound_lock = threading.Lock()

        # Flag para controlar o modo paralelo
        self.parallel_mode = False

        # Pilha para salvar estados do modo paralelo
        self.parallel_mode_stack = []

        # Flag para uso temporário do modo paralelo (blocos específicos)
        self.temp_parallel_mode = False

        # Perfil harmônico para síntese aditiva
        self.harmonic_profile = self.PERFIS_INSTRUMENTOS[self.instrumento_atual]["harmonic_profile"]

    def _carregar_perfil_instrumento(self, nome_instrumento):
        """
        Carrega as configurações de um instrumento específico.

        Args:
            nome_instrumento: Nome do instrumento a ser carregado
        """
        if nome_instrumento in self.PERFIS_INSTRUMENTOS:
            perfil = self.PERFIS_INSTRUMENTOS[nome_instrumento]
            self.waveform = perfil["waveform"]
            self.attack = perfil["attack"]
            self.decay = perfil["decay"]
            self.sustain = perfil["sustain"]
            self.release = perfil["release"]
            self.harmonic_profile = perfil["harmonic_profile"]
            return True
        else:
            print(f"Aviso: Instrumento '{nome_instrumento}' não encontrado. Usando piano como padrão.")
            # Carregar perfil do piano se o instrumento solicitado não existir
            if nome_instrumento != "piano":
                self._carregar_perfil_instrumento("piano")
            return False

    def configurar_instrumento(self, instrumento):
        """
        Configura o instrumento a ser usado para síntese.

        Args:
            instrumento: Nome do instrumento ('piano', 'guitarra', 'violino', etc.)

        Returns:
            True se o instrumento foi configurado com sucesso, False caso contrário
        """
        if instrumento in self.PERFIS_INSTRUMENTOS:
            self.instrumento_atual = instrumento
            self._carregar_perfil_instrumento(instrumento)
            print(f"Instrumento configurado: {instrumento} - {self.PERFIS_INSTRUMENTOS[instrumento]['description']}")
            return True
        else:
            print(
                f"Aviso: Instrumento '{instrumento}' não reconhecido. Instrumentos disponíveis: {', '.join(self.PERFIS_INSTRUMENTOS.keys())}"
            )
            return False

    def tocar_nota(self, frequencia, duracao, volume=0.5):
        """
        Toca uma nota musical com a frequência e duração especificadas.

        Args:
            frequencia: Frequência da nota em Hz
            duracao: Duração da nota em segundos
            volume: Volume da nota (0.0 a 1.0)
        """
        # Converter para lista se for um único valor
        if not isinstance(frequencia, list):
            frequencia = [frequencia]

        # Se for uma única frequência, usar o método padrão
        if len(frequencia) == 1:
            self._tocar_nota_unica(frequencia[0], duracao, volume)
        else:
            # Se for múltiplas frequências (acorde), usar método polifônico
            self._tocar_acorde(frequencia, duracao, volume)

    def _tocar_nota_unica(self, frequencia, duracao, volume=0.5):
        """
        Toca uma única nota musical.

        Args:
            frequencia: Frequência da nota em Hz
            duracao: Duração da nota em segundos
            volume: Volume da nota (0.0 a 1.0)
        """
        n_samples = int(duracao * self.sample_rate)

        # Converter tempos de envelope para amostras
        attack_samples = int(self.attack * self.sample_rate)
        decay_samples = int(self.decay * self.sample_rate)
        release_samples = int(self.release * self.sample_rate)

        # Garantir que os tempos de envelope não excedam a duração total
        total_envelope = attack_samples + decay_samples + release_samples
        if total_envelope > n_samples:
            # Reduzir proporcionalmente mantendo a forma geral
            ratio = n_samples / total_envelope
            attack_samples = int(attack_samples * ratio)
            decay_samples = int(decay_samples * ratio)
            release_samples = int(release_samples * ratio)

        # Calcular o tempo de sustain
        sustain_samples = n_samples - (attack_samples + decay_samples + release_samples)

        # Inicializar array com zeros
        arr = np.zeros(n_samples)

        # Gerar a forma de onda base de acordo com o tipo selecionado e aplicar harmônicos
        t = np.arange(n_samples) / self.sample_rate

        # Síntese aditiva com harmônicos específicos do instrumento selecionado
        for amplitude, harmonic in self.harmonic_profile:
            if self.waveform == "sine":
                arr += amplitude * np.sin(2 * np.pi * frequencia * harmonic * t)
            elif self.waveform == "square":
                arr += amplitude * np.sign(np.sin(2 * np.pi * frequencia * harmonic * t))
            elif self.waveform == "triangle":
                arr += amplitude * (
                    2 * np.abs(2 * (t * frequencia * harmonic - np.floor(t * frequencia * harmonic + 0.5))) - 1
                )
            elif self.waveform == "sawtooth":
                arr += amplitude * (2 * (t * frequencia * harmonic - np.floor(t * frequencia * harmonic + 0.5)))

        # Normalizar o array para evitar clipping
        arr = arr / max(np.max(np.abs(arr)), 1)

        # Criar envelope ADSR
        envelope = np.ones(n_samples)

        # Attack (fade in)
        if attack_samples > 0:
            envelope[:attack_samples] = np.linspace(0, 1, attack_samples)

        # Decay (redução até o nível de sustain)
        if decay_samples > 0:
            envelope[attack_samples : attack_samples + decay_samples] = np.linspace(1, self.sustain, decay_samples)

        # Sustain (nível constante)
        if sustain_samples > 0:
            envelope[attack_samples + decay_samples : attack_samples + decay_samples + sustain_samples] = self.sustain

        # Release (fade out)
        if release_samples > 0:
            envelope[-release_samples:] = np.linspace(self.sustain, 0, release_samples)

        # Aplicar envelope
        arr = arr * envelope

        # Normalizar e ajustar volume
        arr = (arr * volume * 32767).astype(np.int16)

        # Criar som a partir do array numpy (estéreo)
        stereo = np.vstack((arr, arr)).T
        sound = pygame.mixer.Sound(buffer=stereo.tobytes())

        # Tocar a nota
        sound.play()

        # Determinar o modo atual (global ou temporário)
        atual_parallel_mode = self.parallel_mode or self.temp_parallel_mode

        if atual_parallel_mode:
            # Em modo paralelo, adicionar o som à lista de sons ativos e iniciar um thread
            # para monitorar quando o som termina
            with self.sound_lock:
                self.active_sounds.append(sound)

            # Criar thread para aguardar a finalização do som
            def wait_for_sound_completion():
                time.sleep(duracao)
                with self.sound_lock:
                    if sound in self.active_sounds:
                        self.active_sounds.remove(sound)

            sound_thread = threading.Thread(target=wait_for_sound_completion)
            sound_thread.daemon = True
            sound_thread.start()
        else:
            # Em modo sequencial tradicional, bloquear até o som terminar
            time.sleep(duracao)

    def _tocar_acorde(self, frequencias, duracao, volume=0.5):
        """
        Toca um acorde (múltiplas frequências simultaneamente).

        Args:
            frequencias: Lista de frequências em Hz
            duracao: Duração do acorde em segundos
            volume: Volume do acorde (0.0 a 1.0)
        """
        n_samples = int(duracao * self.sample_rate)

        # Converter tempos de envelope para amostras
        attack_samples = int(self.attack * self.sample_rate)
        decay_samples = int(self.decay * self.sample_rate)
        release_samples = int(self.release * self.sample_rate)

        # Garantir que os tempos de envelope não excedam a duração total
        total_envelope = attack_samples + decay_samples + release_samples
        if total_envelope > n_samples:
            ratio = n_samples / total_envelope
            attack_samples = int(attack_samples * ratio)
            decay_samples = int(decay_samples * ratio)
            release_samples = int(release_samples * ratio)

        # Calcular o tempo de sustain
        sustain_samples = n_samples - (attack_samples + decay_samples + release_samples)

        # Inicializar array com zeros
        arr = np.zeros(n_samples)

        # Gerar e somar todas as formas de onda com os harmônicos do instrumento
        t = np.arange(n_samples) / self.sample_rate

        # Para cada frequência do acorde
        for freq in frequencias:
            # Para cada harmônico no perfil do instrumento
            for amplitude, harmonic in self.harmonic_profile:
                if self.waveform == "sine":
                    arr += amplitude * np.sin(2 * np.pi * freq * harmonic * t)
                elif self.waveform == "square":
                    arr += amplitude * np.sign(np.sin(2 * np.pi * freq * harmonic * t))
                elif self.waveform == "triangle":
                    arr += amplitude * (2 * np.abs(2 * (t * freq * harmonic - np.floor(t * freq * harmonic + 0.5))) - 1)
                elif self.waveform == "sawtooth":
                    arr += amplitude * (2 * (t * freq * harmonic - np.floor(t * freq * harmonic + 0.5)))

        # Normalizar o array para evitar clipping
        arr = arr / max(np.max(np.abs(arr)), 1)

        # Criar envelope ADSR
        envelope = np.ones(n_samples)

        # Attack (fade in)
        if attack_samples > 0:
            envelope[:attack_samples] = np.linspace(0, 1, attack_samples)

        # Decay (redução até o nível de sustain)
        if decay_samples > 0:
            envelope[attack_samples : attack_samples + decay_samples] = np.linspace(1, self.sustain, decay_samples)

        # Sustain (nível constante)
        if sustain_samples > 0:
            envelope[attack_samples + decay_samples : attack_samples + decay_samples + sustain_samples] = self.sustain

        # Release (fade out)
        if release_samples > 0:
            envelope[-release_samples:] = np.linspace(self.sustain, 0, release_samples)

        # Aplicar envelope
        arr = arr * envelope

        # Normalizar e ajustar volume
        arr = (arr * volume * 32767).astype(np.int16)

        # Criar som a partir do array numpy (estéreo)
        stereo = np.vstack((arr, arr)).T
        sound = pygame.mixer.Sound(buffer=stereo.tobytes())

        # Tocar o acorde
        sound.play()

        # Determinar o modo atual (global ou temporário)
        atual_parallel_mode = self.parallel_mode or self.temp_parallel_mode

        if atual_parallel_mode:
            # Em modo paralelo, adicionar o som à lista de sons ativos e iniciar um thread
            with self.sound_lock:
                self.active_sounds.append(sound)

            # Criar thread para aguardar a finalização do som
            def wait_for_sound_completion():
                time.sleep(duracao)
                with self.sound_lock:
                    if sound in self.active_sounds:
                        self.active_sounds.remove(sound)

            sound_thread = threading.Thread(target=wait_for_sound_completion)
            sound_thread.daemon = True
            sound_thread.start()
        else:
            # Em modo sequencial tradicional, bloquear até o som terminar
            time.sleep(duracao)

    def pausa(self, duracao):
        """
        Realiza uma pausa (silêncio) com a duração especificada.

        Args:
            duracao: Duração da pausa em segundos
        """
        time.sleep(duracao)

    def configurar_envelope(self, attack=None, decay=None, sustain=None, release=None):
        """
        Configura os parâmetros do envelope ADSR.

        Args:
            attack: Tempo de ataque em segundos
            decay: Tempo de decaimento em segundos
            sustain: Nível de sustentação (0.0 a 1.0)
            release: Tempo de liberação em segundos
        """
        if attack is not None:
            self.attack = attack
        if decay is not None:
            self.decay = decay
        if sustain is not None:
            self.sustain = sustain
        if release is not None:
            self.release = release

    def configurar_forma_onda(self, waveform):
        """
        Configura a forma de onda a ser usada na síntese.

        Args:
            waveform: Tipo de forma de onda ("sine", "square", "triangle" ou "sawtooth")
        """
        formas_validas = ["sine", "square", "triangle", "sawtooth"]
        if waveform.lower() in formas_validas:
            self.waveform = waveform.lower()
        else:
            print(f"Aviso: Forma de onda '{waveform}' não reconhecida. Usando 'sine' como padrão.")
            self.waveform = "sine"

    def habilitar_modo_paralelo(self, status=True):
        """
        Ativa ou desativa o modo de reprodução paralela de sons.

        Args:
            status: True para habilitar, False para desabilitar o modo paralelo
        """
        self.parallel_mode = status
        print(f"Modo de reprodução paralela: {'Ativado' if status else 'Desativado'}")

    def salvar_estado_paralelo(self):
        """
        Salva o estado atual do modo paralelo na pilha.
        Útil para blocos de código onde o modo paralelo é temporariamente alterado.
        """
        self.parallel_mode_stack.append(self.parallel_mode)

    def restaurar_estado_paralelo(self):
        """
        Restaura o último estado do modo paralelo salvo na pilha.
        """
        if self.parallel_mode_stack:
            self.parallel_mode = self.parallel_mode_stack.pop()
            print(f"Modo de reprodução paralela restaurado: {'Ativado' if self.parallel_mode else 'Desativado'}")
        else:
            print("Aviso: Tentativa de restaurar estado paralelo sem estado salvo anteriormente")

    def ativar_paralelo_temporario(self):
        """
        Ativa temporariamente o modo de reprodução paralela para um bloco específico.
        """
        self.temp_parallel_mode = True
        print("Modo paralelo temporário: Ativado")

    def desativar_paralelo_temporario(self):
        """
        Desativa o modo de reprodução paralela temporário e aguarda a conclusão dos sons ativos.
        """
        self.temp_parallel_mode = False
        print("Modo paralelo temporário: Desativado")

    def interromper_todos_sons(self):
        """
        Interrompe todos os sons que estão tocando atualmente.
        """
        with self.sound_lock:
            for sound in self.active_sounds:
                sound.stop()
            self.active_sounds = []

    def aguardar_todos_sons(self):
        """
        Espera até que todos os sons ativos terminem de tocar.
        """
        while True:
            with self.sound_lock:
                if not self.active_sounds:
                    break
            # Pequena pausa para evitar consumo excessivo de CPU
            time.sleep(0.1)
