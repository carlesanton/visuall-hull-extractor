#version 330 compatibility
in vec2 pixel_pos_in_cam_1;
// in vec2 pixel_pos_in_cam_2;
uniform sampler2D model_cam_1_image;
// uniform sampler2D model_cam_2_image;
vec4 in_shilouete_1;
// vec4 in_shilouete_2;
// float is_painted;

void main() {
    in_shilouete_1 = texture(model_cam_1_image, pixel_pos_in_cam_1);
    // in_shilouete_2 = float(texture(model_cam_2_image, pixel_pos_in_cam_2));
    // in_shilouete_1 = vec4(pixel_pos_in_cam_1, 0.,1.);
    // in_shilouete_2 = vec4(pixel_pos_in_cam_2, 0.,1.);
    // is_painted = in_shilouete_1 * in_shilouete_2;
    // gl_FragColor = vec4(pixel_pos_in_cam_1/5000,1.0,1.);
    gl_FragColor = in_shilouete_1;
}