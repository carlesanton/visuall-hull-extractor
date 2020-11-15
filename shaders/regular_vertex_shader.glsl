#version 330 compatibility
in vec3 vert;
in vec3 input_color;
out vec3 color;
void main(){
    color = input_color;
    gl_Position = gl_ModelViewProjectionMatrix * vec4(vert, 1.0); 
}