#version 330 core

in float i_time;
in vec2 i_mouse;
in vec2 i_resolution;

float WEAVE_SCALE = 5.0;

const float NOISE_V_SCALE = 150.0;      /* >1.0 */
const float NOISE_H_SCALE = 1.0;        /* >1.0 */
const float NOISE_DARK_COEFF = 0.025;   /* 0.0 - 1.0 */
const float NOISE_LIGHT_COEFF = 0.045;  /* 0.0 - 1.0 */

const float AO_COEFF = 0.4;             /* 0.0 - 1.0 */

const float TILT_X = -0.25;
const float TILT_Y = -0.5;

const float WARP_SPEED = 0.25;

const vec3 black = vec3(0.145);         /* dark weave color */
const vec3 gray  = vec3(0.225);         /* light weave color */

//==============================================================================

float hash(vec2 p) { return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453123); }

float noise(vec2 p) {
    vec2 i = floor(p);
    vec2 f = fract(p);

    float a = hash(i);
    float b = hash(i + vec2(1.0, 0.0));
    float c = hash(i + vec2(0.0, 1.0));
    float d = hash(i + vec2(1.0, 1.0));

    vec2 u = f * f * (3.0 - 2.0 * f);
    return mix(a, b, u.x) +
        (c - a) * u.y * (1.0 - u.x) +
        (d - b) * u.x * u.y;
}

//==============================================================================

mat3 rotX(float tilt) {
    return mat3(
        1.0, 0.0, 0.0,
        0.0, cos(tilt), -sin(tilt),
        0.0, sin(tilt), cos(tilt)
    );
}

mat3 rotY(float tilt) {
    return mat3(
        cos(tilt), 0.0, sin(tilt),
        0.0, 1.0, 0.0,
        -sin(tilt), 0.0, cos(tilt)
    );
}

//==============================================================================

void tilt(inout vec2 uv, inout vec3 normal) {
    float z = 1.0 + TILT_X * uv.x + TILT_Y * uv.y;
    uv /= z;
    normal = normalize(normal * rotY(-TILT_Y) * rotX(-TILT_X));
}

//==============================================================================

void warp(inout vec2 uv, inout vec3 normal) {
    float t = i_time * WARP_SPEED;
    float wave = (
        sin(uv.x * 3.5 + t * 1.1) * 0.01 + 
        sin((uv.x + uv.y) * 2.5 + t * 1.3) * 0.03 + 
        sin((uv.x - uv.y) * 3.0 - t * 0.7) * 0.02
    );
    uv += vec2(wave * 0.5, wave);
}

//==============================================================================

vec2 getTwillUv(vec2 uv) {
    float weave_size = i_resolution.x / i_resolution.y;

    vec2 twill_uv = fract(uv * weave_size * WEAVE_SCALE);
    return vec2(
        fract(twill_uv.x + 0.25 * floor(twill_uv.y / 0.25)),
        fract(twill_uv.y + 0.25 * floor(twill_uv.x / 0.25))
    );
}

//==============================================================================

vec3 getTwillAlbedo(vec2 tex_uv, vec2 twill_uv) {
    float twill_pattern = step(0.5, twill_uv.x);
    float v_noise = noise(tex_uv * vec2(NOISE_V_SCALE * WEAVE_SCALE, NOISE_H_SCALE * WEAVE_SCALE));
    float h_noise = noise(tex_uv * vec2(NOISE_H_SCALE * WEAVE_SCALE, NOISE_V_SCALE * WEAVE_SCALE));
    
    return mix(
        black + NOISE_DARK_COEFF * (v_noise - 0.5),
        gray + NOISE_LIGHT_COEFF * (h_noise - 0.5),
        twill_pattern
    );
}

//==============================================================================

vec3 getTwillNormalMap(vec3 surface_normal, vec2 twill_uv) {            
    float x_angle = step(0.5, twill_uv.x) * sin((mod(twill_uv.x, 0.5) - 0.25) * 3.14);
    float y_angle = (1.0 - step(0.5, twill_uv.y)) * sin((twill_uv.y - 0.25) * 3.14);
    float z_angle = twill_uv.x < 0.5 ? sin((twill_uv.y + 0.25) * 3.14) 
        : sin((mod(twill_uv.x, 0.5) + 0.25) * 3.14);
    
    return normalize(vec3(x_angle, y_angle, z_angle) + surface_normal);
}

//==============================================================================

float getTwillAOMap(vec2 twill_uv) {
    float AO = twill_uv.x < 0.5 ? sin(twill_uv.y * 2.0 * 3.14) 
        : sin(mod(twill_uv.x, 0.5) * 2.0 * 3.14);
    return (AO * AO_COEFF) + (1.0 - AO_COEFF);
}

//==============================================================================

void main() {   
    vec2 uv = gl_FragCoord.xy / max(i_resolution.x, i_resolution.y);
    vec3 normal = vec3(0.0, 0.0, 1.0);
    warp(uv, normal);
    tilt(uv, normal);
    
    vec2 twill_uv = getTwillUv(uv);   
    vec3 twill_normal = getTwillNormalMap(normal, twill_uv);
    vec3 twill_albedo = getTwillAlbedo(uv, twill_uv);
    float twill_ao = getTwillAOMap(twill_uv);
    
    vec3 diffuse_position = vec3(2.0 * (i_mouse.xy / i_resolution.xy) - vec2(1.0), 1.0);
    vec3 diffuse_direction = normalize(diffuse_position);
    vec3 diffuse_light = max(dot(twill_normal, diffuse_direction), 0.0) * vec3(1.0, 1.0, 1.0);
    
    gl_FragColor = vec4(clamp(0.6 + 0.75 * diffuse_light, 0.0, 1.0) * twill_albedo * twill_ao, 1.0);
}

//==============================================================================