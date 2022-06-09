import numpy as np
from PIL import Image, ImageDraw
import math

def padding(R):

    X=[]
    for _ in range(len(R)):
        for _ in range(len(R[0])):
            Y=[0]
        X.append(Y)
    first_row=np.append(X,R,axis=1)
    last_row=np.append(first_row,X,axis=1)

    X=[]
    for _ in range(len(last_row[0])):
        X.append(0)
    first_col=np.append([X],last_row,axis=0)
    last_col=np.append(first_col,[X],axis=0)

    return last_col

def filter():
    h=np.array([[1,0,-1],
                [2,0,-2],
                [1,0,-1]])
    
    v=np.array([[1,2,1],
                [0,0,0],
                [-1,-2,-1]])
    
    return h,v


def convolution(R):
    pa_R=padding(R) 
    R=pa_R
    h,v=filter()
    convol_h=[]
    convol_v=[]
    for i in range(len(R)-2):
        convol_v_1=[]
        convol_h_1=[]
        for j in range(len(R[0])-2):
            convol_h_1.append(np.sum(R[i:i+3:,j:j+3:]*h))
            convol_v_1.append(np.sum(R[i:i+3:,j:j+3:]*v))
        convol_h.append(convol_h_1)
        convol_v.append(convol_v_1)
    convol_h=np.array(convol_h)
    convol_v=np.array(convol_v)

    return convol_v,convol_h

def Gussian_filter():
    h=np.array([1,2,1])/4
    
    v=np.array([1,2,1]).T/4
    return h,v

def Gaussian_blur(R):
    pa_R=padding(R)
    R=pa_R
    h,v=Gussian_filter()
    row=[]
    for i in range(len(R)-2):
        cols=[]
        for j in range(len(R[0])-2):
            col=R[i:i+3:,j:j+3:]@h@v
            cols.append(col)
        row.append(cols)
    row=np.array(row)
    return row

def Rs_make(image,R):

    corner_number = 0
    real_corner = 0
    corner_coordinate = []
    real_corner_coordinate = []
    
    pixel=np.array(image)
    a,b=convolution(R)
    x=Gaussian_blur(a)
    y=Gaussian_blur(b)
    
    dx=x*x
    dxy=x*y
    dy=y*y
    
    dx2=Gaussian_blur(dx)
    dxy2=Gaussian_blur(dxy)
    dy2=Gaussian_blur(dy)

##M's no need to calculate. it is garbage . so if you want to delete this, you can remove     
    M=np.array([[dx2,dxy2],[dxy2,dy2]])  
    
    detM=dx2*dy2-dxy2**2
    trM=(dx2+dy2)**2
    
    Rs=detM-0.06*trM    ## you can change the number among 0.04~0.06.
    for i in range(len(Rs)):
        for j in range(len(Rs[0])):
## sometimes image pixel has 4 dimension. so i use "if" and "else"
            if len(pixel[0][0])==4:
                if Rs[i][j]>5.1*10**7:  ## 5.1*10**7 is threshold. if you want to change , you can change threshold
                    # pixel[i][j]=[255,0,0,255] ## corner points are red 
                    corner_coordinate.append([i, j])
                    corner_number += 1
            elif len(pixel[0][0])==3:
                if Rs[i][j]>5.1*10**8:  ## 5.1*10**7 is threshold. if you want to change , you can change threshold
                    # pixel[i][j]=[255,0,0] ## corner points are red 
                    corner_coordinate.append([i, j])
                    corner_number += 1
    
    boundary = 20
                    
    for start in corner_coordinate :
        for end in corner_coordinate[:] :
            if (abs(end[0] - start[0]) < boundary and abs(end[1] - start[1]) < boundary and start != end) :
                corner_coordinate.remove(end)
                
    return pixel, real_corner, corner_coordinate

    
if __name__ == '__main__' :
    image=Image.open('./data/harriscorner.png')
    image_pixel=np.array(image)
    R=[]
    for i in range(len(image_pixel)):
        R2=[]
        for j in range(len(image_pixel[0])):
                R2.append(image_pixel[i][j][0])
        R.append(R2)
    R=np.array(R)

    result_image, result_corner, result_coordinate = Rs_make(image,R)

    im=Image.fromarray(result_image)
    draw = ImageDraw.Draw(im)
    for coor in result_coordinate :
        draw.ellipse((coor[1] - 5, coor[0] - 5, 
                    coor[1] + 5, coor[0] + 5),
                    outline='red')

    im.show()
    im.save('save.png')

    print(len(result_coordinate))
    print('hello world')