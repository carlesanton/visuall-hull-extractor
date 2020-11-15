#version 330 compatibility
in vec3 vert;

// Vhull variables
uniform mat4 view_matrix_model_cam_1;
uniform mat4 view_matrix_model_cam_2;
uniform vec2 modeling_cam_1_focal_length;
uniform vec2 modeling_cam_2_focal_length;
uniform vec2 modeling_cam_1_image_center;
uniform vec2 modeling_cam_2_image_center;

out vec2 pixel_in_uv_coord_cam_1;
out vec2 pixel_in_uv_coord_cam_2;

void main(){

    vec4 point_in_cam1_coordinates = view_matrix_model_cam_1 * vec4(vert, 1.0);
    vec2 pixel_pos_in_cam_1 = vec2(
        modeling_cam_1_image_center.x + modeling_cam_1_focal_length.x * point_in_cam1_coordinates.x / point_in_cam1_coordinates.z, 
        modeling_cam_1_image_center.y + modeling_cam_1_focal_length.y * point_in_cam1_coordinates.y / point_in_cam1_coordinates.z);
    
    vec4 point_in_cam2_coordinates = view_matrix_model_cam_2 * vec4(vert, 1.0);
    vec2 pixel_pos_in_cam_2 = vec2(
        modeling_cam_2_image_center.x + modeling_cam_2_focal_length.x * point_in_cam2_coordinates.x / point_in_cam2_coordinates.z, 
        modeling_cam_2_image_center.y + modeling_cam_2_focal_length.y * point_in_cam2_coordinates.y / point_in_cam2_coordinates.z);

    vec2 image_size = modeling_cam_1_image_center*2;

    pixel_in_uv_coord_cam_1 = vec2(pixel_pos_in_cam_1.x/image_size.x , pixel_pos_in_cam_1.y/image_size.y);
    pixel_in_uv_coord_cam_2 = vec2(pixel_pos_in_cam_2.x/image_size.x , pixel_pos_in_cam_2.y/image_size.y);
    gl_Position = gl_ModelViewProjectionMatrix * vec4(vert, 1.0); 
}