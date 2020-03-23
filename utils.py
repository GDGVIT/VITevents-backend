# Comperator for Row segmentation

def compare(i,j):
    if j <= i+30 and j >= i-30:
        return True
    else:
        return False