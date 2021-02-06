import shutil

import group
import image
import lines
import points
import poly_lines
import rectilinear 
import structured 
import unstructured 
import lowlevel

def testit(test):
    try:
        test()
    except:
        print("  FAILED")

def clean_all():
    group.clean()
    image.clean()
    lines.clean()
    points.clean()
    poly_lines.clean()
    rectilinear.clean()
    structured.clean()
    unstructured.clean()
    lowlevel.clean()
    try:
        shutil.rmtree("__pycache__")
    except:
        pass
    
def test_all():
    testit(group.run)
    testit(image.run)
    testit(lines.run)
    testit(points.run)
    testit(poly_lines.run)
    testit(rectilinear.run)
    testit(structured.run)
    testit(unstructured.run)
    testit(lowlevel.run)

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        opt = sys.argv[1]
    else:
        opt = "-"
    
    if (opt == "run"):
        test_all()
    elif (opt == "clean"):
        clean_all()
    else:
        print("UNKNOWN OPTION: " + opt)
        print("USE: python runall.py [run|clean]")
        
    print("*** ALL DONE ***")

