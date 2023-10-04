#! usr/bin/python3.9
import turtle
import Space_Partition as sp


def draw_tree(root) -> None:
    """
    This function can use turtle to draw a binary tree
    """

    def height(head):
        return 1 + max(height(node) for node in head.child_nodes) if len(head.child_nodes) > 0 else -1

    def jump_to(x, y):
        t.penup()
        t.goto(x, y)
        t.pendown()

    def draw(node, x, y, dx):
        if node:
            t.goto(x, y)
            jump_to(x, y - 20)
            t.write(len(node.assigned_dimension), align="center")
            # t.write(len(node.assigned_seed), align="center")
            n = len(node.child_nodes)
            width = dx * 2
            delta_x = width / (n - 1)
            pos_x = x - dx - delta_x
            pos_y = y - 60
            for node in node.child_nodes:
                draw(node, pos_x := pos_x + delta_x, pos_y, dx / (n + 1))
                jump_to(x, y - 20)

    t = turtle.Turtle()
    t.speed(0)
    turtle.delay(0)
    h = height(root)
    jump_to(0, 30 * h)
    draw(root, 10 * h, 0, 130 * h)
    t.hideturtle()
    turtle.mainloop()

if __name__ == '__main__':
    draw_tree(sp.init_partition(seeds_num=4).child_nodes[0])