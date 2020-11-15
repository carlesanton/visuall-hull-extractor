#version 330 compatibility
in vec3 vert;
void main(){
    gl_Position = gl_ModelViewProjectionMatrix * vec4(vert, 1.0);
}