#include <stdio.h>
#include <stdlib.h>
#include <SDL2/SDL.h>
#include <math.h>

//--------------------------FONCTIONS POUR LES DESSINS AVEC CURSEUR----------------------------------------

void drawCursor(SDL_Renderer* renderer, int x, int y) {
    SDL_Rect cursor = {x, y, 5, 5};
    SDL_SetRenderDrawColor(renderer, 0, 255, 0, 255); // Curseur vert
    SDL_RenderFillRect(renderer, &cursor);
}

void drawAnimatedLine(SDL_Renderer* renderer, int x1, int y1, int x2, int y2, int thickness) {
    float dx = x2 - x1;
    float dy = y2 - y1;
    float steps = fmax(fabs(dx), fabs(dy));
    float xIncrement = dx / steps;
    float yIncrement = dy / steps;
    float x = x1, y = y1;

    for (int i = 0; i < steps; i++) {
        drawCursor(renderer, (int)x, (int)y); // Dessiner avec le curseur
        SDL_RenderPresent(renderer);
        SDL_Delay(10);  // Ajuster pour contrôler la vitesse du dessin
        x += xIncrement;
        y += yIncrement;
    }
}

void drawAnimatedSquare(SDL_Renderer* renderer, int x, int y, int sideLength) {
    for (int i = 0; i < sideLength; i++) {
        drawCursor(renderer, x + i, y); // Dessiner le haut
        SDL_RenderPresent(renderer);
        SDL_Delay(10);
    }
    for (int i = 0; i < sideLength; i++) {
        drawCursor(renderer, x + sideLength, y + i); // Dessiner la droite
        SDL_RenderPresent(renderer);
        SDL_Delay(10);
    }
    for (int i = 0; i < sideLength; i++) {
        drawCursor(renderer, x + sideLength - i, y + sideLength); // Dessiner le bas
        SDL_RenderPresent(renderer);
        SDL_Delay(10);
    }
    for (int i = 0; i < sideLength; i++) {
        drawCursor(renderer, x, y + sideLength - i); // Dessiner la gauche
        SDL_RenderPresent(renderer);
        SDL_Delay(10);
    }
}

void drawAnimatedCircle(SDL_Renderer* renderer, int centerX, int centerY, int radius) {
    for (int angle = 0; angle < 360; angle++) {
        float rad = angle * (M_PI / 180.0f);
        int x = centerX + (int)(radius * cos(rad));
        int y = centerY + (int)(radius * sin(rad));
        drawCursor(renderer, x, y); // Placer le curseur
        SDL_RenderPresent(renderer);
        SDL_Delay(5);  // Ajuster pour la vitesse du tracé
    }
}

//---------------------------------------------------------------------------------------------

int main(int argc, char *argv[]) {
    if (SDL_Init(SDL_INIT_VIDEO) < 0) { return 1; }

    SDL_Window* window = SDL_CreateWindow("Animation avec Curseur",
                                          SDL_WINDOWPOS_UNDEFINED, SDL_WINDOWPOS_UNDEFINED,
                                          640, 480, SDL_WINDOW_SHOWN);
    SDL_Renderer* renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED);

    SDL_SetRenderDrawColor(renderer, 0, 0, 0, 255);
    SDL_RenderClear(renderer);
drawAnimatedSquare(renderer, 100, 100, 100);
SDL_Delay(500);
drawAnimatedCircle(renderer, 300, 300, 50);
SDL_Delay(500);
drawAnimatedLine(renderer, 50, 50, 300, 300, 10);




    SDL_RenderPresent(renderer); // Présenter le rendu final

    SDL_Delay(20000); // Pause de 20 secondes avant de quitter

    SDL_DestroyRenderer(renderer);
    SDL_DestroyWindow(window);
    SDL_Quit();

    return 0;
}
