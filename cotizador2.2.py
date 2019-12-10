# -*- coding: utf-8 -*-
"""
Created on Wed Jan 11 16:04:47 2017

@author: Rvaldez
"""

import tkinter as TKI;
import tkinter.ttk as ttk;


import Fun_22 as FUN;

def Dialog1Display():
    Dialog1 = TKI.Tk()
    Dialog1.geometry("700x700")

    ####################################################### Principales 
   
    limite_cobertura = float(eP1.get())
    deducible_Gen = float(eP2.get())
    
    nro_tit_solo = float(eSAH1.get())
    nro_tit_mu = float(eSAH2.get())
    nro_tit_mf = float(eSAH3.get())
    
    factor_tit_mu = float(eSAM1.get())
    factor_tit_mf = float(eSAM2.get()) 
    
    
    ######################################################## Amb - Hosp   
    limite_cobertura_Amb = float(eA1.get())
    deducible_Amb = float(eA2.get())
    p_Amb = float(eA3.get())
    limite_ambulancia = float(eA4.get())
        
    limite_cobertura_Hos = float(eH1.get())      
    deducible_Hos = float(eH2.get())     
    p_Hos = float(eH3.get())  
    limite_copago_Hos = float(eH4.get())
    cuart_aliment = float(eH5.get())
    
    ########################################################### Materinidad    
    
    limite_cobertura_Mat = eM1.get()  
    
    if limite_cobertura_Mat == '':          #Con esto fijamos para que si el usuarion no ingresa una frecuencia de maternidad, esta es 0
        limite_cobertura_Mat = 0 
        deducible_Mat = 0   
        p_Mat = 0     
        
        
           
    else:
        limite_cobertura_Mat = float(limite_cobertura_Mat) 
        deducible_Mat = float(eM2.get())     
        p_Mat = float(eM3.get())      
        
                
    ########################################################### Preexistencias   
    
    limite_cobertura_Prex = ePRE1.get()  
    
    if limite_cobertura_Prex == '':          #Con esto fijamos para que si el usuarion no ingresa una frecuencia de Preexistencias, esta es 0
        limite_cobertura_Prex = 0    
                  
    else:
        limite_cobertura_Prex = float(limite_cobertura_Prex)        
          
    
    ##################################################################### Adicionales     
    
    my_iter = int(ePS1.get())
    seed = int(ePS2.get())
    
    #################################################################### Calculo
    
    #Datos de la base internos en el cotizador
    edad_pro_H = 38
    edad_pro_M = 37
    ptgH = 1
    ptgM = 1 - ptgH
    mean_N_Prex = 0
    prob_perdida = 0.4
    factor_real_ts = 1
    factor_real_tmu = 2.093
    factor_real_tmf = 3.77
    frec_ambulancia =  0.0558 
    
    #Calculos
    res_H = FUN.pp_func(limite_cobertura, deducible_Gen, edad_pro_H, 'Hombre', limite_cobertura_Amb, deducible_Amb, p_Amb, limite_cobertura_Hos, deducible_Hos,\
                        p_Hos, limite_copago_Hos, cuart_aliment, limite_cobertura_Mat, deducible_Mat, p_Mat, limite_cobertura_Prex, mean_N_Prex,\
                        prob_perdida, my_iter, seed)
                        
    res_M = FUN.pp_func(limite_cobertura, deducible_Gen, edad_pro_M, 'Mujer', limite_cobertura_Amb, deducible_Amb, p_Amb, limite_cobertura_Hos, deducible_Hos,\
                        p_Hos, limite_copago_Hos, cuart_aliment, limite_cobertura_Mat, deducible_Mat, p_Mat, limite_cobertura_Prex, mean_N_Prex,\
                        prob_perdida, my_iter, seed)  
                        
        
    PPm = res_H[0]*ptgH + res_M[0]*ptgM
    PPp = res_H[1]*ptgH + res_M[1]*ptgM 
    PP = max(PPm,PPp) + frec_ambulancia*limite_ambulancia  #Se añaden las cob adicionales
    
    ptg_ts = nro_tit_solo/(nro_tit_solo + nro_tit_mu + nro_tit_mf)
    ptg_tmu = nro_tit_mu/(nro_tit_solo + nro_tit_mu + nro_tit_mf)
    ptg_tmf = nro_tit_mf/(nro_tit_solo + nro_tit_mu + nro_tit_mf)
    
    PPteo = ptg_ts*PP*factor_real_ts + ptg_tmu*PP*factor_real_tmu + ptg_tmf*PP*factor_real_tmf  #se nivela la tarifa en base al número de titulares y dependientes y el factor t1 y tf      
    PP_a = PPteo/(ptg_ts + ptg_tmu*factor_tit_mu + ptg_tmf*factor_tit_mf)   
    
        
    MyText = "La prima pura para un titular solo es:        {0}\n\
La prima pura para un titular más uno es:     {1}\n\
La prima pura para un titular más familia es: {2}".format(PP_a, PP_a*factor_tit_mu, PP_a*factor_tit_mf)  
    T = TKI.Text(Dialog1, height=3, width=200)
    T.grid(row=0,column=0)
    T.insert(TKI.INSERT, MyText)      

    




############################################################################################################################################
###################################################################################################### Fronting

master = TKI.Tk()
master.title("Cotizador Med. Prepagada (beta1)")
master.geometry("1200x610")

####################################################################################################### Principales
lfdata = ttk.Labelframe(master, padding=(6, 6, 12, 12), text='Caracteristicas Principales del Plan')
lfdata.grid(row=0, column=0, rowspan=2, columnspan=2, sticky='nsew')
TKI.Label(lfdata, text="Límite Máximo por Persona-Año: ").grid(row=0, column=0, sticky=TKI.E)
TKI.Label(lfdata, text="Deducible General: ").grid(row=1, column=0, sticky=TKI.E)
eP1 = TKI.Entry(lfdata)
eP1.grid(row=0, column=1)
eP2 = TKI.Entry(lfdata)
eP2.grid(row=1, column=1)


###################################################################################################### Ambulatorio
lfdata2 = ttk.Labelframe(master, padding=(6, 6, 12, 12), text='Cobertura Ambulatoria')
lfdata2.grid(row=2, column=0, rowspan=4, columnspan=2, sticky='nsew')
TKI.Label(lfdata2, text="Límite de Cobertura Ambulatorio: ").grid(row=0, column=0, sticky=TKI.E)
TKI.Label(lfdata2, text="Deducible Ambulatorio: ").grid(row=1, column=0, sticky=TKI.E)
TKI.Label(lfdata2, text="Porc. Copago Ambulatorio: ").grid(row=2, column=0, sticky=TKI.E)
TKI.Label(lfdata2, text="Límite Ambulancia por Emergencia: ").grid(row=3, column=0, sticky=TKI.E)
eA1 = TKI.Entry(lfdata2)
eA1.grid(row=0, column=1)
eA2 = TKI.Entry(lfdata2)
eA2.grid(row=1, column=1)
eA3 = TKI.Entry(lfdata2)
eA3.grid(row=2, column=1)
eA4 = TKI.Entry(lfdata2)
eA4.grid(row=3, column=1)

############################################################################################### Hospitalario
lfdata3 = ttk.Labelframe(master, padding=(6, 6, 12, 12), text='Cobertura Hospitalaria')
lfdata3.grid(row=6, column=0, rowspan=5, columnspan=2, sticky='nsew')
TKI.Label(lfdata3, text="Límite de Cobertura Hospitalario: ").grid(row=0, column=0, sticky=TKI.E)
TKI.Label(lfdata3, text="Deducible Hospitalario: ").grid(row=1, column=0, sticky=TKI.E)
TKI.Label(lfdata3, text="Porc. Copago Hospitalario: ").grid(row=2, column=0, sticky=TKI.E)
TKI.Label(lfdata3, text="Limite Copago Hospitalario: ").grid(row=3, column=0, sticky=TKI.E)
TKI.Label(lfdata3, text="Cuarto y Alimento: ").grid(row=4, column=0, sticky=TKI.E)
eH1 = TKI.Entry(lfdata3)    #Limite
eH1.grid(row=0, column=1)
eH2 = TKI.Entry(lfdata3)    #Deducible
eH2.grid(row=1, column=1)
eH3 = TKI.Entry(lfdata3)    #Copago en %
eH3.grid(row=2, column=1)
eH4 = TKI.Entry(lfdata3)    #Limite Copago
eH4.grid(row=3, column=1)
eH5 = TKI.Entry(lfdata3)    #Cuarto y alimento
eH5.grid(row=4, column=1)

############################################################################################### Maternidad
lfdata4 = ttk.Labelframe(master, padding=(6, 6, 12, 12), text='Cobertura Maternidad')
lfdata4.grid(row=11, column=0, rowspan=3, columnspan=2, sticky='nsew')
TKI.Label(lfdata4, text="Límite de Cobertura Maternidad: ").grid(row=0, column=0, sticky=TKI.E)
TKI.Label(lfdata4, text="Deducible Maternidad: ").grid(row=1, column=0, sticky=TKI.E)
TKI.Label(lfdata4, text="Porc. Copago Maternidad: ").grid(row=2, column=0, sticky=TKI.E)
eM1 = TKI.Entry(lfdata4)  #Limite Mat
eM1.grid(row=0, column=1)
eM2 = TKI.Entry(lfdata4) #Deducible Mat
eM2.grid(row=1, column=1)
eM3 = TKI.Entry(lfdata4) #Copago en % Mat
eM3.grid(row=2, column=1)


############################################################################################### Preexistnecias
lfdata5 = ttk.Labelframe(master, padding=(6, 6, 12, 12), text='Cobertura Preexistencias')
lfdata5.grid(row=14, column=0, rowspan=1, columnspan=2, sticky='nsew')
TKI.Label(lfdata5, text="Límite de Cobertura Preexistencias: ").grid(row=0, column=0, sticky=TKI.E)
ePRE1 = TKI.Entry(lfdata5)  #Limite Preex
ePRE1.grid(row=0, column=1)



########################################################################################################## 2da columna
########################################################################################################## Datos de la empresa
lfdataS1 = ttk.Labelframe(master, padding=(6, 6, 12, 12), text='Datos Empresa')
lfdataS1.grid(row=0, column=2, rowspan=3, columnspan=4, sticky='nsew')
TKI.Label(lfdataS1, text="Número de Titulares Solos: ").grid(row=0, column=0, sticky=TKI.E)
TKI.Label(lfdataS1, text="Número de Titulares más Uno: ").grid(row=1, column=0, sticky=TKI.E)
TKI.Label(lfdataS1, text="Número de Titulares más Familia: ").grid(row=2, column=0, sticky=TKI.E)

eSAH1 = TKI.Entry(lfdataS1) #Titular Solo
eSAH1.grid(row=0, column=1) 
eSAH2 = TKI.Entry(lfdataS1) #Titular mas uno
eSAH2.grid(row=1, column=1)
eSAH3 = TKI.Entry(lfdataS1) #Titular mas familia
eSAH3.grid(row=2, column=1)


TKI.Label(lfdataS1, text="Factor: ").grid(row=1,column=2, sticky=TKI.E)
TKI.Label(lfdataS1, text="Factor: ").grid(row=2,column=2, sticky=TKI.E)
eSAM1 = TKI.Entry(lfdataS1) #Factor tit mas uno
eSAM1.grid(row=1, column=3)
eSAM2 = TKI.Entry(lfdataS1) #Factor tit mas familia
eSAM2.grid(row=2, column=3)

########################################################################################################## Datos Generales
lfdataDG = ttk.Labelframe(master, padding=(6, 6, 12, 12), text='Parámetros Simulación')
lfdataDG.grid(row=3, column=2, rowspan=3, columnspan=3, sticky='nsew')
TKI.Label(lfdataDG, text="Número de Iteraciones: ").grid(row=0, column=0, sticky=TKI.E)
TKI.Label(lfdataDG, text="Seed: ").grid(row=1, column=0, sticky=TKI.E)
button = TKI.Button(lfdataDG, text = 'Simular', command = Dialog1Display)
ePS1 = TKI.Entry(lfdataDG)
ePS1.grid(row=0, column=1)
ePS2 = TKI.Entry(lfdataDG)
ePS2.grid(row=1, column=1)
button.grid(row=1, column=2)

TKI.mainloop( )