# -*- coding: utf-8 -*-
##############################################################################
#    Web PDF Report to Print
#    Copyright 2014 Raphael Rodrigues <raphael0608@gmail.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    "name": "Report to Print",
    'version': '1.0',
    'category': 'Web',
    'description': """Web PDF Report to Print

Print PDF Preview report in your browser.

* For IE, Adobe Reader is required.
* For Chrome , nothing is requried.
* For Firefox, Adobe Reader is required.


If your brower prevented pop-up window, you should allow it.

    PDF

    """,
    'author': 'raphael0608@gmail.com',
    'license': 'AGPL-3',
    'depends': ['web'],
    'data': [
        'views/web_pdf_preview.xml',
    ],
}

