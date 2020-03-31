import pygame

import properties


def main():
    pygame.init()
    pygame.display.set_mode((properties.width, properties.height))

    while True:
        cont = handle_event(pygame.event.wait())
        if not cont:
            break


def handle_event(e) -> bool:
    print(e)
    if e.type == pygame.QUIT:
        return False
    return True


if __name__ == '__main__':
    main()
