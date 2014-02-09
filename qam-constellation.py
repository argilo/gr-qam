# Copyright 2014 Clayton Smith
#
# This file is part of qam-tx
#
# qam-tx is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# qam-tx is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with qam-tx; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.

table = """110,111 111,011 010,111 011,011 100,101 101,111 110,101 111,111
110,100 111,000 010,100 011,000 100,000 101,010 110,000 111,010
100,111 101,011 000,111 001,011 000,101 001,111 010,101 011,111
100,100 101,000 000,100 001,000 000,000 001,010 010,000 011,010
010,011 011,001 000,011 001,001 000,001 001,101 100,001 101,101
010,110 011,100 000,110 001,100 000,010 001,110 100,010 101,110
110,011 111,001 100,011 101,001 010,001 011,101 110,001 111,101
110,110 111,100 100,110 101,100 010,010 011,110 110,010 111,110"""

rows = table.split("\n")[::-1]
table2 = [row.split(" ") for row in rows]
table3 = [[int(cell.replace(",",""),2) for cell in row] for row in table2]
for x in range(64):
    for row in range(8):
        for col in range(8):
            if table3[row][col] == x:
                print str(col*8 + row) + ",",
