#include <stdio.h>
#include <stdlib.h>
#include <SDL2/SDL.h>
#include <math.h>

//--------------------------FONCTIONS POUR LES DESSINS----------------------------------------

// Fonction d'animation pour dessiner un point
void animation(SDL_Renderer* renderer, int x, int y, int delay) {
    SDL_RenderDrawPoint(renderer, x, y);  // Dessine le point
    SDL_RenderPresent(renderer);          // Met à jour l'affichage
    SDL_Delay(delay);                     // Pause pour l'animation
}

// Fonction pour dessiner une ligne animée
void drawLine(SDL_Renderer* renderer, int x1, int y1, int x2, int y2, int thickness, int delay) {
    SDL_SetRenderDrawColor(renderer, 255, 255, 0, 255); // Couleur jaune par défaut
    float dx = x2 - x1;
    float dy = y2 - y1;
    float length = sqrt(dx * dx + dy * dy);

    if (length != 0) {
        dx /= length;
        dy /= length;
    }

    // Dessine chaque point de la ligne
    for (int i = 0; i < length; i++) {
        int x = x1 + (int)(dx * i);
        int y = y1 + (int)(dy * i);

        // Dessine la ligne avec animation
        SDL_SetRenderDrawColor(renderer, 255, 255, 0, 255); // Couleur jaune par défaut
        for (int j = -thickness / 2; j <= thickness / 2; j++) {
            int offsetX = (int)(dy * j);
            int offsetY = (int)(-dx * j);
            animation(renderer, x + offsetX, y + offsetY, delay); // Utilise animation pour chaque point
        }
    }
}

// Fonction pour dessiner un carré animé
void drawSquare(SDL_Renderer* renderer, int x, int y, int sideLength, int thickness, int delay) {
    // Dessine les quatre côtés du carré avec animation
    drawLine(renderer, x, y, x + sideLength, y, thickness, delay); // Haut
    drawLine(renderer, x + sideLength, y, x + sideLength, y + sideLength, thickness, delay); // Droit
    drawLine(renderer, x + sideLength, y + sideLength, x, y + sideLength, thickness, delay); // Bas
    drawLine(renderer, x, y + sideLength, x, y, thickness, delay); // Gauche
}

// Fonction pour dessiner un rectangle animé
void drawRectangle(SDL_Renderer* renderer, int x, int y, int width, int height, int thickness, int delay) {
    // Dessine les quatre côtés du rectangle avec animation
    drawLine(renderer, x, y, x + width, y, thickness, delay); // Haut
    drawLine(renderer, x + width, y, x + width, y + height, thickness, delay); // Droit
    drawLine(renderer, x + width, y + height, x, y + height, thickness, delay); // Bas
    drawLine(renderer, x, y + height, x, y, thickness, delay); // Gauche
}

// Fonction pour dessiner un losange animé
void drawRhombus(SDL_Renderer* renderer, int x, int y, int diagonal1, int diagonal2, int thickness, int delay) {
    int halfD1 = diagonal1 / 2;
    int halfD2 = diagonal2 / 2;

    // Dessine les quatre côtés du losange
    drawLine(renderer, x, y - halfD2, x + halfD1, y, thickness, delay); // Haut gauche
    drawLine(renderer, x + halfD1, y, x, y + halfD2, thickness, delay); // Bas gauche
    drawLine(renderer, x, y + halfD2, x - halfD1, y, thickness, delay); // Bas droit
    drawLine(renderer, x - halfD1, y, x, y - halfD2, thickness, delay); // Haut droit
}

// Fonction pour dessiner un triangle équilatéral animé
void drawTriangle(SDL_Renderer* renderer, int x, int y, int sideLength, int thickness, int delay) {
    int height = (int)(sideLength * sqrt(3) / 2); // Hauteur du triangle équilatéral

    // Dessine les trois côtés du triangle
    drawLine(renderer, x, y, x + sideLength, y, thickness, delay); // Base
    drawLine(renderer, x + sideLength, y, x + sideLength / 2, y - height, thickness, delay); // Côté droit
    drawLine(renderer, x + sideLength / 2, y - height, x, y, thickness, delay); // Côté gauche
}

// Fonction pour dessiner un triangle rectangle animé
void drawRightTriangle(SDL_Renderer* renderer, int x, int y, int base, int height, int thickness, int delay) {
    // Dessine les trois côtés du triangle rectangle
    drawLine(renderer, x, y, x + base, y, thickness, delay); // Base
    drawLine(renderer, x + base, y, x + base, y - height, thickness, delay); // Hauteur
    drawLine(renderer, x + base, y - height, x, y, thickness, delay); // Hypoténuse
}

// Fonction pour dessiner un parallélogramme animé
void drawParallelogram(SDL_Renderer* renderer, int x, int y, int base, int height, int angle, int thickness, int delay) {
    // Calcul des décalages pour dessiner les parallélogrammes
    int offsetX = (int)(height * tan(angle * M_PI / 180));

    // Dessine les quatre côtés du parallélogramme
    drawLine(renderer, x, y, x + base, y, thickness, delay); // Bas
    drawLine(renderer, x + base, y, x + base + offsetX, y - height, thickness, delay); // Droit
    drawLine(renderer, x + base + offsetX, y - height, x + offsetX, y - height, thickness, delay); // Haut
    drawLine(renderer, x + offsetX, y - height, x, y, thickness, delay); // Gauche
}

// Fonction pour dessiner un trapèze animé
void drawTrapezium(SDL_Renderer* renderer, int x, int y, int topBase, int bottomBase, int height, int thickness, int delay) {
    int offsetX = (int)((bottomBase - topBase) / 2.0);

    // Dessine les quatre côtés du trapèze
    drawLine(renderer, x, y, x + topBase, y, thickness, delay); // Haut
    drawLine(renderer, x + topBase, y, x + bottomBase - offsetX, y + height, thickness, delay); // Droit
    drawLine(renderer, x + bottomBase - offsetX, y + height, x + offsetX, y + height, thickness, delay); // Bas
    drawLine(renderer, x + offsetX, y + height, x, y, thickness, delay); // Gauche
}

// Fonction pour dessiner un polygone avec animation
void drawPolygon(SDL_Renderer* renderer, int centerX, int centerY, int radius, int sides, int thickness, int delay) {
    if (sides < 5) {
        printf("Le nombre de côtés doit être supérieur ou égal à 5.\n");
        return;
    }

    double angleStep = 2 * M_PI / sides;  // Calcul de l'angle entre les sommets

    // Calcul des coordonnées des sommets
    int startX = centerX + radius * cos(0);
    int startY = centerY + radius * sin(0);

    int prevX = startX;
    int prevY = startY;

    // Dessine chaque côté du polygone avec animation
    for (int i = 1; i <= sides; i++) {
        int x = centerX + radius * cos(i * angleStep);
        int y = centerY + radius * sin(i * angleStep);

        // Utilise drawLine avec animation pour dessiner chaque côté
        drawLine(renderer, prevX, prevY, x, y, thickness, delay);
        prevX = x;
        prevY = y;
    }

    // Dernière ligne pour fermer le polygone
    drawLine(renderer, prevX, prevY, startX, startY, thickness, delay);
}

//---------------------------------------------------------------------------------------------

int main(int argc, char *argv[]) {
        // LES PREREQUIS POUR FAIRE APPARAITRE L'INTERFACE DE DESSIN---------------------------
    if (SDL_Init(SDL_INIT_VIDEO) < 0) {
        printf("Erreur lors de l'initialisation de SDL: %s\n", SDL_GetError());
        return 1;
    }

    SDL_Window* window = SDL_CreateWindow("Animation de Formes",
                                          SDL_WINDOWPOS_UNDEFINED, SDL_WINDOWPOS_UNDEFINED,
                                          640, 480, SDL_WINDOW_SHOWN);
    if (!window) {
        printf("Erreur de création de la fenêtre: %s\n", SDL_GetError());
        SDL_Quit();
        return 1;
    }

    SDL_Renderer* renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED);
    if (!renderer) {
        printf("Erreur de création du renderer: %s\n", SDL_GetError());
        SDL_DestroyWindow(window);
        SDL_Quit();
        return 1;
    }

    SDL_SetRenderDrawColor(renderer, 0, 0, 0, 255); // Fond noir pour la fenêtre
    SDL_RenderClear(renderer);      // Efface l'écran

    // Affichage des dessins ------------------------------------------------------------------

    // Dessiner les formes animées
    // drawSquare(renderer, 100, 100, 200, 5, 1);
    // SDL_Delay(500);
    // drawRectangle(renderer, 50, 50, 200, 100, 5, 1);
    // SDL_Delay(500);
    // drawRhombus(renderer, 300, 150, 100, 100, 5, 1);
    // SDL_Delay(500);
    // drawTriangle(renderer, 100, 300, 200, 5, 1);
    // SDL_Delay(500);
    // drawRightTriangle(renderer, 400, 300, 200, 100, 5, 1);
    // SDL_Delay(500);
    // drawParallelogram(renderer, 100, 450, 200, 100, 30, 5, 1);
    // SDL_Delay(500);
    // drawTrapezium(renderer,100 , 300, 150, 400, 100, 5, 1);
    // SDL_Delay(500);
    drawPolygon(renderer, 320, 240, 100, 8, 5, 1); // Octogone 




    SDL_RenderPresent(renderer); // Présente le rendu final

    SDL_Delay(5000); // Pause de 5 secondes avant de quitter

    SDL_DestroyRenderer(renderer);
    SDL_DestroyWindow(window);
    SDL_Quit();

    return 0;
}