#include <iostream>

#include <GL/gl.h>
#include <GL/glext.h>
#include <GL/glu.h>

#include <GLFW/glfw3.h>

int main(int argc, const char* argv[])
{
    GLFWwindow* fwWindow;

    if (!glfwInit())
        return -1;
    
    glfwWindowHint(GLFW_DOUBLEBUFFER, 1);
    glfwWindowHint(GLFW_SAMPLES, 8);
    glfwWindowHint(GLFW_RESIZABLE, 0);

    fwWindow = glfwCreateWindow(640, 480, "Computer Graphics Assignment Framework", NULL, NULL);

    if (!fwWindow)
    {
        glfwTerminate();
        return -1;
    }

    glfwMakeContextCurrent(fwWindow);
    
    glClearColor(0.0, 0.0, 0.0, 0.0);

    while (!glfwWindowShouldClose(fwWindow))
    {
        glClear(GL_COLOR_BUFFER_BIT);
        
        glBegin(GL_TRIANGLES);
            glColor3d(1.0, 0.0, 0.0);
            glVertex3d(0.0, 0.0, 0.0);
            glColor3d(0.0, 1.0, 0.0);
            glVertex3d(1.0, 0.0, 0.0);
            glColor3d(0.0, 0.0, 1.0);
            glVertex3d(0.0, 1.0, 0.0);
        glEnd();

        glfwSwapBuffers(fwWindow);

        glfwPollEvents();
    }

    glfwTerminate();

    return 0;   
}
