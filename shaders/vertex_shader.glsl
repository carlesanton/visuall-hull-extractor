#version 330 core

attribute vec3 vert;
uniform mat4 model_matrix;
uniform mat4 view_matrix_viewing_cam;
uniform mat4 projection_matrix_viewing_cam;

uniform vec2 modeling_cam_1_focal_length;
uniform vec2 modeling_cam_2_focal_length;
uniform vec2 modeling_cam_1_image_center;
uniform vec2 modeling_cam_2_image_center;
uniform mat4 view_matrix_model_cam_1;
uniform mat4 view_matrix_model_cam_2;

uniform mat4 mvp;
out vec2 pixel_pos_in_cam_1;
out vec2 pixel_pos_in_cam_2;

void main() {
    vec4 point_in_cam1_coordinates = view_matrix_model_cam_1 * vec4(vert, 1.0);
    pixel_pos_in_cam_1 = vec2(modeling_cam_1_image_center.x + modeling_cam_1_focal_length.x * point_in_cam1_coordinates.x / point_in_cam1_coordinates.z, modeling_cam_1_image_center.y + modeling_cam_1_focal_length.y * point_in_cam1_coordinates.y / point_in_cam1_coordinates.z);
    
    vec4 point_in_cam2_coordinates = view_matrix_model_cam_2 * vec4(vert, 1.0);
    pixel_pos_in_cam_2 = vec2(modeling_cam_2_image_center.x + modeling_cam_2_focal_length.x * point_in_cam2_coordinates.x / point_in_cam2_coordinates.z, modeling_cam_2_image_center.y + modeling_cam_2_focal_length.y * point_in_cam2_coordinates.y / point_in_cam2_coordinates.z);
    
    gl_Position = projection_matrix_viewing_cam * view_matrix_viewing_cam * model_matrix * vec4(vert, 1.0);
}
