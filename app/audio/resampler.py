import numpy as np
from scipy.signal import resample_poly


def resample_audio(
    audio_data: bytes,
    input_rate: int,
    output_rate: int,
) -> bytes:
    audio = np.frombuffer(audio_data, dtype=np.int16)

    resampled = resample_poly(
        audio,
        output_rate,
        input_rate,
    )

    resampled = np.clip(
        resampled,
        -32768,
        32767,
    ).astype(np.int16)

    return resampled.tobytes()