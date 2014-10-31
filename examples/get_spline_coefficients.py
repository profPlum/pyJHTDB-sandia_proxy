#! /usr/bin/env python
########################################################################
#
#  Copyright 2014 Johns Hopkins University
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Contact: turbulence@pha.jhu.edu
# Website: http://turbulence.pha.jhu.edu/
#
########################################################################

import argparse

from pyJHTDB.interpolator import spline_interpolator as si
from pyJHTDB.dbinfo import isotropic1024coarse, mhd1024, channel

def write_coefficients(
        info = None,
        n = 1,
        m = 1):
    i = si(info, n = n, m = m)
    for coord in ['x', 'y', 'z']:
        for order in range(i.m+1):
            text_file = open(
                    (info['name']
                    + '_' + coord
                    + 'spline_m{0}q{1:0>2}_d{2}_coeff.csv'.format(i.m, i.n*2 + 2, order)),
                    'w')
            if info[coord + 'periodic']:
                for point in range(len(i.spline[coord].beta[0][order])):
                    text_file.write('0, {0}'.format(i.spline[coord].neighbour_list[0][point]))
                    for c in i.spline[coord].beta[0][order][point].coef:
                        text_file.write(', {0}'.format(c))
                    text_file.write('\r\n')
            else:
                for node in range(len(i.spline[coord].beta)):
                    for point in range(len(i.spline[coord].beta[node][order])):
                        if (i.spline[coord].beta[node][order][point].coef.shape[0] > 1
                             or (not( i.spline[coord].beta[node][order][point].coef[0] == 0.0))):
                            text_file.write('{0}, {1}'.format(node, i.spline[coord].neighbour_list[node][point]))
                            for c in i.spline[coord].beta[node][order][point].coef:
                                text_file.write(', {0}'.format(c))
                            if i.spline[coord].beta[node][order][point].coef.shape[0] < i.m*2 + 2 - order:
                                for tcounter in range(i.m*2 + 2
                                        - order - i.spline[coord].beta[node][order][point].coef.shape[0]):
                                    text_file.write(', 0')
                            text_file.write('\r\n')
            text_file.close()
    return None

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
            description = 'write coefficients of spline polynomials for the channel flow database.')
    parser.add_argument(
            '-q',
            '--kernel-size',
            type = int,
            dest = 'q',
            default = 4,
            metavar = 'Q',
            help = ('Base kernel size used in the computation, must be an even number; '
                  + 'Q-1 will be the kernel size close enough to the boundary in the y direction.'))
    parser.add_argument(
            '-m',
            '--smoothness',
            type = int,
            dest = 'm',
            default = 1,
            metavar = 'M',
            help = ('Number of continuous derivatives for the resulting spline.'))
    opt = parser.parse_args()
    if opt.q % 2 == 1:
        print('please provide an even value of Q.')
        exit()
    write_coefficients(info = channel, n = (opt.q-2)/2, m = opt.m)

