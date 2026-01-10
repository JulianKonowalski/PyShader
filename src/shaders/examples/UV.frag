#version 330 core

in vec3 i_position;
in vec3 i_normal;
in vec2 i_tex_coord;

void main() {
    gl_FragColor = vec4(i_tex_coord, 0.0, 1.0);
}