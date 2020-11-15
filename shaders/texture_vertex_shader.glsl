#version 330 compatibility
in vec3 vert;
in vec2 vertexUV;
out vec2 UV;
void main(){
    gl_Position = gl_ModelViewProjectionMatrix * vec4(vert, 1.0); 
    UV = vertexUV;
}