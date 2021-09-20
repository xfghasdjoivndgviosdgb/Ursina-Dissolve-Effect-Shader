from ursina import *

dissolve=Shader(language=Shader.GLSL,fragment="""
#version 400


uniform sampler2D p3d_Texture0;
uniform sampler2D noiseTex;
uniform float threshold;

in vec2 uv;

out vec4 color;

void main(){
    float noiseVal=texture(noiseTex,uv).x;
    if(noiseVal>=threshold){
        color=vec4(0,0,0,0);
    }
    else{
        float final_alpha=1;
        float alphaVal=threshold-noiseVal;
        if(alphaVal<=0.1){
            color=vec4(0.3,1,1,(alphaVal*5)/2);       //change the color for the dissolving effect over here. first three values are for the color.
        }
        else{
            color=texture(p3d_Texture0,uv);
        }
    }
}

""")


if __name__=="__main__":
    from ursina import *
    threshold=1

    def update():
        global threshold
        e.set_shader_input("threshold",threshold)
        if threshold>0 and held_keys["space"]:
            threshold-=time.dt/10       #change the divisor to slow down or speed up the effect


    app=Ursina()
    e=Entity(model="cube",texture="brick")
    e.shader=dissolve
    e.set_shader_input("noiseTex",load_texture("noise2.png"))       #put your texture here
    plyer=EditorCamera()
    app.run()
