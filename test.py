import re
from processing.file_handler_processor import FileHandlerProcessor

# Exemplo de uso
code = """
// test
# teste
using GSIFuncoes;
using Pottencial.Core.DTO;
using Pottencial.GG.Business.LimiteTaxa;
using Pottencial.GG.DTO;
using Pottencial.GG.DTO.FormalizacaoLimiteTaxa;
using Pottencial.GG.DTO.LimiteTaxa;
using Pottencial.GG.Util.Enums;
using Serilog;
using System;
using System.Collections.Generic;
using System.IO;
using System.Net;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Reflection;
using System.Text;
using System.Threading.Tasks;
using System.Web.Http;
using System.Web.UI.WebControls;

public class Example {
    // Your code here
}
"""
processor = FileHandlerProcessor()
processor.initialize(code)
processed_code = processor.process()
print(processed_code)