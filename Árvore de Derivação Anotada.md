                                                    expressao_magica
                                         {p[0] = ('binop', 'et', ('unary', ...), ('binop', ...))}
                                                            |
                              ----------------------------------------------------------
                              |                             |                          |
                       expressao_magica                     ET                 expressao_magica
                  {p[0]=('unary', 'maxima', (...))}        (et)        {p[0]=('binop', 'intra', (...), (...))}
                              |                                                        |
                    --------------------                              ---------------------------------
                    |                  |                              |               |               |
              INTENSIDADE       expressao_magica               expressao_magica      INTRA    expressao_magica
                (maxima)    {p[0]=('spell', 'fira',         {p[0]=('spell', 'aqua', (intra) {p[0]=('spell', 'terra',
                             None, ['danum'])}               'matera', ['curam'])}            None, ['sonium','reparo'])}
                                       |                              |                               |
                                 encantamento                   encantamento                    encantamento
                          {p[0]=('spell', 'fira',      {p[0]=('spell', 'aqua',        {p[0]=('spell', 'terra',
                           None, ['danum'])}             'matera', ['curam'])}          None, ['sonium', 'reparo'])}
                                       |                              |                               |
                            -------------------           -------------------------       -------------------------
                            |                 |           |             |         |       |                       |
                        ELEMENTO        lista_efeitos ELEMENTO        ESTADO  lista_efeitos ELEMENTO         lista_efeitos
                         (fira)         {p[0]=['danum']} (aqua)     (matera) {p[0]=['curam']} (terra)   {p[0]=['sonium','reparo']}
                                             |                                    |                               |
                                           EFEITO                              EFEITO               -------------------
                                           (danum)                             (curam)              |                 |
                                                                                                  EFEITO        lista_efeitos
                                                                                                  (sonium)      {p[0]=['reparo']}
                                                                                                                     |
                                                                                                                  EFEITO
                                                                                                                  (reparo)


Sentença de Entrada: maxima fira danum et aqua matera curam intra terra sonium reparo
