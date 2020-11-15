#version 330 compatibility
in vec3 vert;

// Vhull variables
uniform mat4 view_matrix_model_cam_1;
uniform mat4 projection_matrix_model_cam_1;


out vec2 pixel_in_uv_coord_cam_1;
out vec2 pixel_in_uv_coord_cam_2;

void main(){

    // vec4 point_in_cam1_coordinates = view_matrix_model_cam_1 * vec4(vert, 1.0);
    vec4 point_in_screen =  vec4(vert, 1.0) * view_matrix_model_cam_1 * projection_matrix_model_cam_1;

    pixel_in_uv_coord_cam_1 = vec2(point_in_screen.x , point_in_screen.y);
    pixel_in_uv_coord_cam_2 = pixel_in_uv_coord_cam_1;
    gl_Position = gl_ModelViewProjectionMatrix * vec4(vert, 1.0); 
}