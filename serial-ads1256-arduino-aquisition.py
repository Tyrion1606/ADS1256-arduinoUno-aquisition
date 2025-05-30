import serial
import argparse
import time

def ler_serial(porta, baudrate, arquivo_saida):
    try:
        ser = serial.Serial(porta, baudrate, timeout=1)
        print(f"[INFO] Conectado na porta {porta} com baudrate {baudrate}")

        with open(arquivo_saida, 'w') as f:
            print(f"[INFO] Gravando dados em: {arquivo_saida}")
            while True:
                if ser.in_waiting > 0:
                    linha = ser.readline().decode('utf-8', errors='replace').strip()
                    timestamp = time.time()
                    f.write(f"{timestamp},{linha}\n")
                    f.flush()
                    print(f"[{timestamp}] {linha}")

    except KeyboardInterrupt:
        print("\n[INFO] Encerrando a leitura.")
    except serial.SerialException as e:
        print(f"[ERRO] Problema na serial: {e}")
    finally:
        if 'ser' in locals() and ser.is_open:
            ser.close()
            print("[INFO] Porta serial fechada.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Leitor de porta serial para arquivo")
    parser.add_argument('--porta', type=str, default='COM3', help='Exemplo: /dev/ttyUSB0 ou COM3')
    parser.add_argument('--baudrate', type=int, default=115200, help='Velocidade da comunicação serial')
    parser.add_argument('--saida', type=str, default='dados_serial.csv', help='Arquivo para salvar os dados')

    args = parser.parse_args()

    ler_serial(args.porta, args.baudrate, args.saida)
