#version 330 core

layout (location = 0) in vec3 pos;
layout (location = 1) in vec3 normal;
layout (location = 2) in vec2 tex_coord;

uniform int     u_frame;
uniform float   u_time;
uniform float   u_time_delta;
uniform vec2    u_mouse;
uniform vec2    u_resolution;

out int     i_frame;
out float   i_time;
out float   i_time_delta;
out vec2    i_mouse;
out vec2    i_resolution;
out vec3    i_normal;
out vec3    i_position;
out vec2    i_tex_coord;

void main() {
    gl_Position = vec4(pos, 1.0);

    i_frame         = u_frame;
    i_time          = u_time;
    i_time_delta    = u_time_delta;
    i_mouse         = u_mouse;
    i_resolution    = u_resolution;
    i_position      = gl_Position.xyz;
    i_normal        = normal;
    i_tex_coord     = tex_coord;
}