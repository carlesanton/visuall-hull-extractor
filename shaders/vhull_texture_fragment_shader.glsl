#version 330 compatibility
    in vec2 pixel_in_uv_coord_cam_1;
    in vec2 pixel_in_uv_coord_cam_2;
    uniform sampler2DArray cam_images;
    vec4 in_shilouete_1;
    vec4 in_shilouete_2;
    float is_painted;
    out vec4 out_color;
    void main(){
        in_shilouete_1 = texture(cam_images, vec3(pixel_in_uv_coord_cam_1,0));
        in_shilouete_2 = texture(cam_images, vec3(pixel_in_uv_coord_cam_2,1));
        // in_shilouete_1 = vec4(pixel_pos_in_cam_1, 0.,1.);
        // in_shilouete_2 = vec4(pixel_pos_in_cam_2, 0.,1.);
        is_painted = dot(in_shilouete_1, in_shilouete_2)/(3.);
        if (is_painted > 1.2)
        // out_color = vec4(pixel_in_uv_coord_cam_1.x,pixel_in_uv_coord_cam_1.y,0.,is_painted);
        // out_color = vec4(0.,0.,0.,is_painted);
            out_color = vec4(is_painted,is_painted,is_painted,is_painted);
            // out_color = in_shilouete_1;
        else
           discard;
        // out_color = out_color_1 + out_color_2;
        // out_color = mix(texture(cam_images, vec3(UV,0)), texture(cam_images, vec3(UV,1)), 0.5);
    }