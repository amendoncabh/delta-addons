/*############################################################################
#    Report to Print
#    Copyright 2017 Raphael Rodrigues <raphael0608@gmail.com>
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
############################################################################*/
odoo.define('report.web_pdf_preview', function (require) {

function is_mobile() {
    return /Android|iPhone|iPad|iPod|Mobi/i.test(navigator.userAgent);
}

/*
 * Hook `session.get_file` in /addons/report/static/src/js/qwebactionmanager.js to prevent downloading.
 */
var session = require('web.session');
var get_file = session.get_file;

session.get_file = function(options) {
    if (!options || options.url !== '/report/download') {
        get_file.apply(this, arguments);
        return;
    }

    var params = {
        data: options.data.data,
        token: new Date().getTime()
    };

    var url = session.url('/report/preview', params);
    
    var printPDF = function(url) {
    	var iframe = this._printIframe;
    	if (!this._printIframe) {
    		iframe = this._printIframe = document.createElement('iframe');
    		document.body.appendChild(iframe);
    		
    		iframe.style.display = 'none';
    		iframe.onload = function() {
    			setTimeout(function() {
    				iframe.focus();
    				iframe.contentWindow.print();
    			}, 1);
    		};
    	}
    	iframe.src = url;
    }

    /*
     * Open the PDF report in current window on mobile (since iPhone prevents
     * openning in new window), while open in new window on desktop.
     */
    if (is_mobile()) {
        require('web.framework').unblockUI();
        location.href = url;
    } else {
        
        printPDF(url);
        if (typeof options.success === 'function') {
            options.success();
        }
        if (typeof options.complete === 'function') {
            options.complete();
        }
    }
};

});
