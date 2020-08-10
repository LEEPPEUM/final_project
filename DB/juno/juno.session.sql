SELECT ds.*,lsp.pclndIndex as priceindex,lsp.pclndChgRt as priceChg, lsp.stdrYear,lsp.stdrMt
FROM (SELECT *, substr(pnu,1,10) as pnux
      FROM DATASETS) as ds INNER JOIN (SELECT * 
                                       FROM LAND_SIDO_ppeum
                                       WHERE CHAR_LENGTH(pnu)=10 and stdrMt = 1 and stdrYear = 2019) as lsp ON  ds.pnux= lsp.pnu;






