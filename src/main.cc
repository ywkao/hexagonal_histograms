#include <stdio.h>
#include <utility>
#include "HGCalCell.h"

int main() {
    printf("Hello World\n");
    HGCalCell cell_helper(100, 10, 10);
    std::pair<double, double> coor = cell_helper.cellUV2XY1(1, 5, 0, 0);
    printf(">>> x = %.2f, y = %.2f\n", coor.first, coor.second);
    return 0;
}
