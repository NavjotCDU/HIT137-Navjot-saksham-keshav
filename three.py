import turtle
import math

def draw_edge(length, depth):
    if depth == 0:
        turtle.forward(length)
        return
    
    segment = length / 3
    
    draw_edge(segment, depth - 1)
    
    turtle.right(60)  
    draw_edge(segment, depth - 1)
    turtle.left(120)  
    draw_edge(segment, depth - 1)
    turtle.right(60) 
    
    draw_edge(segment, depth - 1)

def draw_polygon(sides, length, depth):
    angle = 360 / sides
    
    for _ in range(sides):
        draw_edge(length, depth)
        turtle.left(angle)  

def main():
    try:
        sides = int(input("Enter the number of sides: "))
        length = float(input("Enter the side length: "))
        depth = int(input("Enter the recursion depth: "))
        
        if sides < 3:
            print("Error: Number of sides must be at least 3.")
            return
        if length <= 0:
            print("Error: Side length must be positive.")
            return
        if depth < 0:
            print("Error: Recursion depth must be non-negative.")
            return
        
        turtle.speed(0)  
        turtle.penup()
        turtle.goto(-length / 2, -length / 2)
        turtle.pendown()
        
        draw_polygon(sides, length, depth)
        
        turtle.done()
        
    except ValueError:
        print("Error: Please enter valid numeric values for sides, length, and depth.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()