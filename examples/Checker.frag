#version 330 core

#define SCALE 10.0
#define COL_1 vec3(0.0, 0.0, 0.0)
#define COL_2 vec3(1.0, 1.0, 1.0)

in vec2 i_tex_coord;
in vec2 i_resolution;

void main() {
    vec2 tex_coord = (gl_FragCoord.xy / i_resolution.x) * SCALE;

    int x_bit = mod(tex_coord.x, 1.0) > 0.5 ? 1 : 0;
    int y_bit = mod(tex_coord.y, 1.0) > 0.5 ? 1 : 0;

    vec3 color = (x_bit == 1 && y_bit == 0) 
        || (x_bit == 0 && y_bit == 1) ? COL_1 : COL_2;

    gl_FragColor = vec4(color, 1.0);
}