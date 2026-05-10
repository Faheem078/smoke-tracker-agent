import wave, struct, math

def generate_siren():
    sample_rate = 44100
    duration = 3.0
    fname = 'alarm.wav'
    wavef = wave.open(fname, 'w')
    wavef.setnchannels(1)
    wavef.setsampwidth(2) 
    wavef.setframerate(sample_rate)

    # Siren: alternates between 1200Hz and 800Hz every 0.3s
    for i in range(int(sample_rate * duration)):
        t = float(i) / sample_rate
        freq = 1200.0 if (t % 0.6) < 0.3 else 800.0
        value = int(32767.0 * math.sin(2.0 * math.pi * freq * t))
        data = struct.pack('<h', value)
        wavef.writeframesraw(data)

    wavef.close()
    print("Created alarm.wav")

if __name__ == "__main__":
    generate_siren()
