#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>

typedef struct {
    int grid_size;
    float coupling;
    int frame_count;
    float accumulator;
} TsotchkeSystem;

TsotchkeSystem* tsotchke_create(int grid_size, float coupling) {
    printf("🚀 Native C initialized: %dx%d\n", grid_size, grid_size);
    TsotchkeSystem *sys = malloc(sizeof(TsotchkeSystem));
    sys->grid_size = grid_size;
    sys->coupling = coupling;
    sys->frame_count = 0;
    sys->accumulator = 0.0f;
    return sys;
}

void tsotchke_destroy(TsotchkeSystem *sys) {
    if (sys) {
        printf("💾 Native destroyed after %d frames\n", sys->frame_count);
        free(sys);
    }
}

float tsotchke_get_collision_risk(TsotchkeSystem *sys) {
    if (!sys) return 0.0f;
    
    float risk = 0.3f + 0.4f * sinf(sys->frame_count * 0.1f);
    sys->accumulator += risk * 0.05f;
    sys->frame_count++;
    
    return fabsf(risk + sys->accumulator * 0.1f);
}
