// Função para gerar relatório em PDF e visualizar impressão
// Sem fazer download do arquivo em PDF

openerp.print_direct = function (instance) {

	instance.web.print_direct = function() { 
	        var self = this;
	        new Model('report.point_of_sale.report_saledetails').call('get_sale_details').then(function(result){
	            var env = {
	                company: self.pos.company,
	                pos: self.pos,
	                products: result.products,
	                payments: result.payments,
	                taxes: result.taxes,
	                total_paid: result.total_paid,
	                date: (new Date()).toLocaleString(),
	            };
	            var report = QWeb.render('SaleDetailsReport', env);
	            self.print_receipt(report);
	        })
	    };
}