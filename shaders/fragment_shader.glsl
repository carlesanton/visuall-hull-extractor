#version 330 core
in vec2 pixel_pos_in_cam_1;
in vec2 pixel_pos_in_cam_2;
uniform sampler2D model_cam_1_image;
uniform sampler2D model_cam_2_image;
float in_shilouete_1;
float in_shilouete_2;
float is_painted;

void main() {
    in_shilouete_1 = float(texture(model_cam_1_image, pixel_pos_in_cam_1));
    in_shilouete_2 = float(texture(model_cam_2_image, pixel_pos_in_cam_2));
    is_painted = in_shilouete_1 * in_shilouete_2;
    gl_FragColor = vec4(1.0,1.0,1.0,1.0);
}