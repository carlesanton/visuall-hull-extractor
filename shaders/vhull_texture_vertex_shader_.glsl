#version 330 compatibility
in vec3 vert;

// Vhull variables
uniform mat4 view_matrix_model_cam_1;
uniform mat4 view_matrix_model_cam_2;
uniform mat4 projection_matrix_model_cam_1;
uniform mat4 projection_matrix_model_cam_2;


out vec2 pixel_in_uv_coord_cam_1;
out vec2 pixel_in_uv_coord_cam_2;

void main(){

    // vec4 point_in_cam1_coordinates = view_matrix_model_cam_1 * vec4(vert, 1.0);
    // vec4 point_in_screen_1 =  projection_matrix_model_cam_1 * view_matrix_model_cam_1 * vec4(vert, 1.0);
    // vec4 point_in_screen_1 =  vec4(vert, 1.0) * view_matrix_model_cam_1 * projection_matrix_model_cam_1;
    vec4 point_in_screen_1 =  projection_matrix_model_cam_1 * view_matrix_model_cam_1 * vec4(vert, 0.0);
    vec4 point_in_screen_2 =  projection_matrix_model_cam_2 * view_matrix_model_cam_2 * vec4(vert, 0.0);

    float a = 100.;
    pixel_in_uv_coord_cam_1 = vec2(-a*point_in_screen_1.x/(320*2) + 0.5, -a*point_in_screen_1.y/(240*2*2));
    pixel_in_uv_coord_cam_2 = vec2(-a*point_in_screen_2.x/(320*2) + 0.5, -a*point_in_screen_2.y/(240*2*2));
    gl_Position = gl_ModelViewProjectionMatrix * vec4(vert, 1.0); 
}