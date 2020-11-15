#version 330 compatibility
    in vec2 UV;
    out vec4 out_color;
    uniform sampler2DArray texture_image;
    void main(){
        vec4 out_color_1 = texture(texture_image, vec3(UV,1));
        vec4 out_color_2 = texture(texture_image, vec3(UV,0));
        out_color = out_color_1 + out_color_2;
        out_color = mix(texture(texture_image, vec3(UV,0)), texture(texture_image, vec3(UV,1)), 0.5);
    }