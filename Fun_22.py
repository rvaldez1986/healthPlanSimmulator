# -*- coding: utf-8 -*-
"""
Created on Tue Feb 06 22:20:25 2018

@author: Rvaldez
"""

import numpy as np;


def pp_func(limite_cobertura, deducible_Gen, edad_pro, genero, limite_cobertura_Amb, deducible_Amb, p_Amb, limite_cobertura_Hos, deducible_Hos,\
    p_Hos, limite_copago_Hos, cuart_aliment, limite_cobertura_Mat, deducible_Mat, p_Mat, limite_cobertura_Prex, mean_N_Prex,\
    prob_perdida, my_iter, seed):
    
    #Obtener parámetros############################################################################################### 
    
    if genero == 'Hombre':
        mean_N_Amb= 0.5
        mean_X_Amb= 1000
        var_X_Amb= 1000000   
        
        mean_N_Hos=0.3
        mean_X_Hos=1000
        var_X_Hos=1000000   
    
        mean_N_Mat_Amb=0
        mean_X_Mat_Amb=1
        var_X_Mat_Amb=1
    
        mean_N_Mat_Hos= 0   
        mean_X_Mat_Hos=1   
        var_X_Mat_Hos=1
    
        
        
    else:
        mean_N_Amb= 1 
        mean_X_Amb= 1000
        var_X_Amb= 1000000   
        
        mean_N_Hos=1
        mean_X_Hos=1000
        var_X_Hos=1000000   
    
        mean_N_Mat_Amb=1
        mean_X_Mat_Amb=1000
        var_X_Mat_Amb=1000000   
    
        mean_N_Mat_Hos= 1  
        mean_X_Mat_Hos=1000   
        var_X_Mat_Hos=1000000   
    
        
    
    ################################################################################## Inicia Calculo

    #Obtenemos la frecuencia por preexistencias ambulatoria y hospitalaria
    mean_N_Prex_Amb = (mean_N_Amb/(mean_N_Amb + mean_N_Hos)) * mean_N_Prex
    mean_N_Prex_Hos = (mean_N_Hos/(mean_N_Amb + mean_N_Hos)) * mean_N_Prex 
    

    # Creamos los arrays    
    Distr_Pagos = np.array([])
    Reclamos_Amb = np.array([])
    Reclamos_Hos = np.array([])
    Reclamos_Mat_Amb = np.array([])
    Reclamos_Mat_Hos = np.array([])
    Reclamos_Prex = np.array([])

    np.random.seed(seed)
    
    ################################################################################## Inicia Calculo
    
    for j in range(0, my_iter):
    
#####################################################################################################################################
#Deducible General
        N_Amb = np.random.binomial(1,mean_N_Amb, 1)             #Nro reclamos ambulatorio
        N_Prex_Amb = np.random.binomial(1,mean_N_Prex_Amb, 1) #Nro reclamos ambulatorio (preexistencias)
        N_Hos = np.random.binomial(1,mean_N_Hos, 1) + np.random.binomial(1,mean_N_Prex_Hos, 1) #Nro reclamos hospitalario
        N_Prex_Hos = np.random.binomial(1,mean_N_Prex_Hos, 1) #Nro reclamos hospitalario (preexistencias)
        N_Mat_Amb = np.random.binomial(1,mean_N_Mat_Amb, 1) #Nro reclamos maternidad Ambulatorio
        N_Mat_Hos = np.random.binomial(1,mean_N_Mat_Hos, 1) #Nro reclamos maternidad Hospitalario
        
        N_Tot = N_Amb + N_Prex_Amb + N_Hos + N_Prex_Hos + N_Mat_Amb + N_Mat_Hos 
        
        theta_Amb = var_X_Amb/mean_X_Amb
        alpha_Amb = mean_X_Amb/theta_Amb
        X_Amb = zip(np.random.gamma(alpha_Amb, theta_Amb, N_Amb), ["Ambulatorio"]*N_Amb[0]) #Valor presentado ambulatorio como tuple
        X_Prex_Amb = zip(np.random.gamma(alpha_Amb, theta_Amb, N_Prex_Amb), ["P Ambulatorio"]*N_Prex_Amb[0]) #Valor presentado preex ambulatorio como tuple
        
        theta_Hos = var_X_Hos/mean_X_Hos
        alpha_Hos = mean_X_Hos/theta_Hos
        X_Hos = zip(np.random.gamma(alpha_Hos, theta_Hos, N_Hos), ["Hospitalario"]*N_Hos[0]) #Valor presentado Hospitalario como tuple 
        X_Prex_Hos = zip(np.random.gamma(alpha_Hos, theta_Hos, N_Prex_Hos), ["P Hospitalario"]*N_Hos[0]) #Valor presentado Hospitalario como tuple 
        
        theta_Mat_Amb = var_X_Mat_Amb/mean_X_Mat_Amb
        alpha_Mat_Amb = mean_X_Mat_Amb/theta_Mat_Amb
        X_Mat_Amb = zip(np.random.gamma(alpha_Mat_Amb, theta_Mat_Amb, N_Mat_Amb), ["Mat Ambulatorio"]*N_Mat_Amb[0]) #Valor presentado maternidad ambulatorio como tuple 
        
        theta_Mat_Hos = var_X_Mat_Hos/mean_X_Mat_Hos
        alpha_Mat_Hos = mean_X_Mat_Hos/theta_Mat_Hos
        X_Mat_Hos = zip(np.random.gamma(alpha_Mat_Hos, theta_Mat_Hos, N_Mat_Hos), ["Mat Hospitalario"]*N_Mat_Hos[0]) #Valor presentado maternidad hosp como tuple  
        
        X_Tot = X_Amb + X_Prex_Amb + X_Hos + X_Prex_Hos + X_Mat_Amb + X_Mat_Hos 
        np.random.shuffle(X_Tot)
        
        if N_Tot[0] > 0:
            Presentado = np.array([x[0] for x in X_Tot]) 
            Coberturas = np.array([x[1] for x in X_Tot]) 
            myd = deducible_Gen
            Myd2 = np.array([])
            PN1 = np.array([])
            for i in range(0, N_Tot):
                PN1 = np.append(PN1, max(Presentado[i] - myd, 0))    
                if PN1[i] == 0:
                    myd = myd - Presentado[i]
                    Myd2 = np.append(Myd2, Presentado[i])
                else:
                    Myd2 = np.append(Myd2, myd)
                    myd = 0 
        
            #Generamos el vector de coberturas y obtenemos el valor después de la cobertura 
            Cubierto = PN1             
            X_Amb2 = Cubierto[Coberturas=="Ambulatorio"]
            X_Prex_Amb2 = Cubierto[Coberturas=="P Ambulatorio"] 
            X_Hos2 = Cubierto[Coberturas=="Hospitalario"]           
            X_Prex_Hos2 = Cubierto[Coberturas=="P Hospitalario"] 
            X_Mat_Amb = Cubierto[Coberturas=="Mat Ambulatorio"]
            X_Mat_Hos = Cubierto[Coberturas=="Mat Hospitalario"]
            
            XT_Amb = np.concatenate((X_Amb2, X_Prex_Amb2), axis=0)
            XT_Hos = np.concatenate((X_Hos2, X_Prex_Hos2), axis=0)
            XT_Mat = np.concatenate((X_Mat_Amb, X_Mat_Hos), axis=0)
            
            n_Amb = len(X_Amb2[X_Amb2>0])
            n_Prex_Amb = len(X_Prex_Amb2[X_Prex_Amb2>0])
            n_Hos = len(X_Hos2[X_Hos2>0])
            n_Prex_Hos = len(X_Prex_Hos2[X_Prex_Hos2>0])            
            n_Mat_Amb = len(X_Mat_Amb[X_Mat_Amb>0])
            n_Mat_Hos = len(X_Mat_Hos[X_Mat_Hos>0])
            
            nt_Amb = n_Amb + n_Prex_Amb
            nt_Hos = n_Hos + n_Prex_Hos
            nt_Mat = n_Mat_Amb + n_Mat_Hos
            
####################################################################################################################################################################################
#Cobertura Ambulatoria               
        
            if nt_Amb>0:          
                Presentado_Amb = XT_Amb        
                Pcob_Amb = [p_Amb]*nt_Amb      #Creamos los vectores con los porcentajes de cobertura que se van a aplicar para hosp y amb
                myd_Amb = deducible_Amb
                Myd2_Amb = np.array([])
                PN1_Amb = np.array([])
                for i in range(0, nt_Amb):    #Ajustamos el impacto del deducible ambulatorio
                    PN1_Amb = np.append(PN1_Amb, max(Presentado_Amb[i] - myd_Amb, 0))    
                    if PN1_Amb[i] == 0:
                        myd_Amb = myd_Amb - Presentado_Amb[i]
                        Myd2_Amb = np.append(Myd2_Amb, Presentado_Amb[i])
                    else:
                        Myd2_Amb = np.append(Myd2_Amb, myd_Amb)
                        myd_Amb = 0 
            
                Pcubierto_Amb = PN1_Amb * Pcob_Amb  #Ajustamos el impacto del porcentaje de cobertura ambulatorio              
                Tot1_Amb = sum(Pcubierto_Amb)
                Tot2_Amb = min(Tot1_Amb, limite_cobertura_Amb)
                n1_Amb = len(Pcubierto_Amb[Pcubierto_Amb>0])  #Puede ser mayor que 1 (incluye preexistencias ambulatorias)
                m_Amb = Tot1_Amb/n1_Amb if n1_Amb > 0 else 0   #ajustamos para no dividir para 0
                rec_elim_Amb = (Tot1_Amb - Tot2_Amb) / (m_Amb) if Tot1_Amb != Tot2_Amb else 0  
                n2_Amb = n1_Amb - np.floor(rec_elim_Amb)   #Puede ser mayor que 1
            
                #Dividir en preexistente y no preexistente
                Tot3_Amb = Tot2_Amb * (mean_N_Amb/(mean_N_Amb + mean_N_Prex_Amb)) if mean_N_Amb + mean_N_Prex_Amb > 0 else 0        #Total pagado ambulatorio neto de preexistencias
                Tot_Prex_Amb = Tot2_Amb * (mean_N_Prex_Amb/(mean_N_Amb + mean_N_Prex_Amb)) if mean_N_Amb + mean_N_Prex_Amb > 0 else 0 #Total pagado por preexistencias ambulatorias
                n3_Amb = min(n2_Amb * (mean_N_Amb/(mean_N_Amb + mean_N_Prex_Amb)) if mean_N_Amb + mean_N_Prex_Amb > 0 else 0, 1)      #Total reclamos ambulatorios sin preexistencias maximo 1 
                n_Prex_Amb2 = min(n2_Amb * (mean_N_Prex_Amb/(mean_N_Amb + mean_N_Prex_Amb)) if mean_N_Amb + mean_N_Prex_Amb > 0 else 0, 1)    #Total reclamos preexistencias ambulatorias maximo 1       
            
            else:       #Si reclamos ambulatorios son 0
                Presentado_Amb = np.array([0])
                Myd2_Amb = np.array([0])
                PN1_Amb = np.array([0])
                Pcob_Amb = np.array([0])
                Pcubierto_Amb = np.array([0])
                #Result_Amb = np.column_stack((Presentado_Amb, Myd2_Amb, PN1_Amb, Pcob_Amb, Pcubierto_Amb))
                Tot1_Amb = 0
                Tot2_Amb = 0
                n1_Amb = 0
                m_Amb = 0
                rec_elim_Amb = 0
                n2_Amb = 0 
                Tot3_Amb = 0
                Tot_Prex_Amb = 0
                n3_Amb = 0
                n_Prex_Amb2 = 0
            
####################################################################################################################################################################################
    #Hospitalario
    
            if nt_Hos>0:
                Presentado_Hos = XT_Hos        
                Pcob_Hos = [p_Hos]*nt_Hos
                myd_Hos = deducible_Hos
                Myd2_Hos = np.array([])
                PN1_Hos = np.array([])
                for i in range(0, nt_Hos):
                    PN1_Hos = np.append(PN1_Hos, max(Presentado_Hos[i] - myd_Hos, 0))    
                    if PN1_Hos[i] == 0:
                        myd_Hos = myd_Hos - Presentado_Hos[i]
                        Myd2_Hos = np.append(Myd2_Hos, Presentado_Hos[i])
                    else:
                        Myd2_Hos = np.append(Myd2_Hos, myd_Hos)
                        myd_Hos = 0 
            
                Pcubierto_Hos = PN1_Hos * Pcob_Hos
                PNocubierto_Hos = PN1_Hos * ([1-p_Hos]*nt_Hos) #Columan % no cubierto 
                #Result_Hos = np.column_stack((Presentado_Hos, Myd2_Hos, PN1_Hos, Pcob_Hos, Pcubierto_Hos, PNocubierto_Hos))
                Tpnocubierto_Hos = sum(PNocubierto_Hos)
                Tot1_Hos = sum(Pcubierto_Hos) + (Tpnocubierto_Hos - limite_copago_Hos if Tpnocubierto_Hos > limite_copago_Hos else 0) #Se añade el impacto del limite de copago
                Tot2_Hos = min(Tot1_Hos, limite_cobertura_Hos)
                n1_Hos = len(Pcubierto_Hos[Pcubierto_Hos>0])
                m_Hos = Tot1_Hos/n1_Hos if n1_Hos > 0 else 0
                rec_elim_Hos = (Tot1_Hos - Tot2_Hos) / (m_Hos) if Tot1_Hos != Tot2_Hos else 0 
                n2_Hos = n1_Hos - np.floor(rec_elim_Hos)
            
                #Dividir en preexistente y no preexistente
                Tot3_Hos = Tot2_Hos * (mean_N_Hos/(mean_N_Hos + mean_N_Prex_Hos)) if mean_N_Hos + mean_N_Prex_Hos > 0 else 0
                Tot_Prex_Hos = Tot2_Hos * (mean_N_Prex_Hos/(mean_N_Hos + mean_N_Prex_Hos)) if mean_N_Hos + mean_N_Prex_Hos > 0 else 0
                n3_Hos = min(n2_Hos * (mean_N_Hos/(mean_N_Hos + mean_N_Prex_Hos)) if mean_N_Hos + mean_N_Prex_Hos > 0 else 0, 1)
                n_Prex_Hos2 = min(n2_Hos * (mean_N_Prex_Hos/(mean_N_Hos + mean_N_Prex_Hos)) if mean_N_Hos + mean_N_Prex_Hos > 0 else 0, 1)
            
            else:
                Presentado_Hos = np.array([0])
                Myd2_Hos = np.array([0])
                PN1_Hos = np.array([0])
                Pcob_Hos = np.array([0])
                Pcubierto_Hos = np.array([0])
                PNocubierto_Hos = np.array([0])            
                #Result_Hos = np.column_stack((Presentado_Hos, Myd2_Hos, PN1_Hos, Pcob_Hos, Pcubierto_Hos))
                Tpnocubierto_Hos = 0
                Tot1_Hos = 0
                Tot2_Hos = 0
                n1_Hos = 0
                m_Hos = 0
                rec_elim_Hos = 0 
                n2_Hos = 0 
                Tot3_Hos = 0
                Tot_Prex_Hos = 0
                n3_Hos = 0
                n_Prex_Hos2 = 0
    
    ##############################################################################################################################################
    #Maternidad            
    
            if nt_Mat>0:                
                Presentado_Mat = XT_Mat       
                Pcob_Mat = [p_Mat]*nt_Mat
                myd_Mat = deducible_Mat
                Myd2_Mat = np.array([])
                PN1_Mat = np.array([])
                for i in range(0, nt_Mat):
                    PN1_Mat = np.append(PN1_Mat, max(Presentado_Mat[i] - myd_Mat, 0))    
                    if PN1_Mat[i] == 0:
                        myd_Mat = myd_Mat - Presentado_Mat[i]
                        Myd2_Mat = np.append(Myd2_Mat, Presentado_Mat[i])
                    else:
                        Myd2_Mat = np.append(Myd2_Mat, myd_Mat)
                        myd_Mat = 0 
    
                Pcubierto_Mat = PN1_Mat * Pcob_Mat
                #Result_Mat = np.column_stack((Presentado_Mat, Myd2_Mat, PN1_Mat, Pcob_Mat, Pcubierto_Mat))
                Tot1_Mat = sum(Pcubierto_Mat)
                Tot2_Mat = min(Tot1_Mat, limite_cobertura_Mat)
                n1_Mat = len(Pcubierto_Mat[Pcubierto_Mat>0])
                m_Mat = Tot1_Mat/n1_Mat if n1_Mat > 0 else 0
                rec_elim_Mat = (Tot1_Mat - Tot2_Mat) / (m_Mat) if Tot1_Mat != Tot2_Mat else 0  
                n2_Mat = n1_Mat - np.floor(rec_elim_Mat) 
            
                #Dividir en ambulatorio y hospitalario            
                Tot3_Mat_Amb = Tot2_Mat * (mean_N_Mat_Amb/(mean_N_Mat_Amb + mean_N_Mat_Hos)) if mean_N_Mat_Amb + mean_N_Mat_Hos > 0 else 0
                Tot3_Mat_Hos = Tot2_Mat * (mean_N_Mat_Hos/(mean_N_Mat_Amb + mean_N_Mat_Hos)) if mean_N_Mat_Amb + mean_N_Mat_Hos > 0 else 0
                n3_Mat_Amb = min(n2_Mat * (mean_N_Mat_Amb/(mean_N_Mat_Amb + mean_N_Mat_Hos)) if mean_N_Mat_Amb + mean_N_Mat_Hos > 0 else 0, 1)
                n3_Mat_Hos = min(n2_Mat * (mean_N_Mat_Hos/(mean_N_Mat_Amb + mean_N_Mat_Hos)) if mean_N_Mat_Amb + mean_N_Mat_Hos > 0 else 0, 1)             
        
            else:                            
                Presentado_Mat = np.array([0])
                Myd2_Mat = np.array([0])
                PN1_Mat = np.array([0])
                Pcob_Mat = np.array([0])
                Pcubierto_Mat = np.array([0])
                #Result_Mat = np.column_stack((Presentado_Mat, Myd2_Mat, PN1_Mat, Pcob_Mat, Pcubierto_Mat))
                Tot1_Mat = 0
                Tot2_Mat = 0
                Tot3_Mat_Amb = 0
                Tot3_Mat_Hos = 0
                n1_Mat = 0
                m_Mat = 0
                rec_elim_Mat = 0 
                n2_Mat = 0  
                n3_Mat_Amb = 0
                n3_Mat_Hos = 0
        
     ##############################################################################################################################################
    #Preexistencias
    
            Tot1_Prex = Tot_Prex_Amb + Tot_Prex_Hos
            Tot2_Prex = min(Tot1_Prex, limite_cobertura_Prex)
            n1_Prex = n_Prex_Amb2 + n_Prex_Hos2
            m_Prex = Tot1_Prex/n1_Prex if n1_Prex > 0 else 0
            rec_elim_Prex = (Tot1_Prex - Tot2_Prex) / (m_Prex) if Tot1_Prex != Tot2_Prex else 0 
            n2_Prex = min(n1_Prex - np.floor(rec_elim_Prex), 1)
         
       
       ###############################################################################################################################################    
    #Conjunto luego de simulacion de amparos individuales (deducible)   
    
            Tot1 = Tot3_Amb + Tot3_Hos + Tot3_Mat_Amb + Tot3_Mat_Hos + Tot2_Prex      
            Tot2 = min(Tot1, limite_cobertura)
                    
        #Ajustamos frecuencia observada
    
            if (n3_Amb + n3_Hos + n3_Mat_Amb + n3_Mat_Hos + n2_Prex)>0:
                ptg_Amb = n3_Amb / (n3_Amb + n3_Hos + n3_Mat_Amb + n3_Mat_Hos + n2_Prex)
                ptg_Hos = n3_Hos / (n3_Amb + n3_Hos + n3_Mat_Amb + n3_Mat_Hos + n2_Prex)        
                ptg_Mat_Amb = n3_Mat_Amb / (n3_Amb + n3_Hos + n3_Mat_Amb + n3_Mat_Hos + n2_Prex)
                ptg_Mat_Hos = n3_Mat_Hos / (n3_Amb + n3_Hos + n3_Mat_Amb + n3_Mat_Hos + n2_Prex)
                ptg_Prex = n2_Prex / (n3_Amb + n3_Hos + n3_Mat_Amb + n3_Mat_Hos + n2_Prex)
                rec_elim = (Tot1 - Tot2) / (ptg_Amb*m_Amb + ptg_Hos*m_Hos + ptg_Mat_Amb*m_Mat + ptg_Mat_Hos*m_Mat + ptg_Prex*m_Prex)
                n4_Amb = min(n3_Amb - np.floor(rec_elim * ptg_Amb), 1)
                n4_Hos = min(n3_Hos - np.floor(rec_elim * ptg_Hos), 1)
                n4_Mat_Amb = min(n3_Mat_Amb - np.floor(rec_elim * ptg_Mat_Amb), 1)
                n4_Mat_Hos = min(n3_Mat_Hos - np.floor(rec_elim * ptg_Mat_Hos), 1)
                n3_Prex = min(n2_Prex - np.floor(rec_elim * ptg_Prex), 1)
            
            else:                                                   #Esto significa que no existen reclamos 
                ptg_Amb = 0
                ptg_Hos = 0       
                ptg_Mat_Amb = 0
                ptg_Mat_Hos = 0
                ptg_Prex = 0
                rec_elim = 0
                n4_Amb = 0
                n4_Hos = 0
                n4_Mat_Amb = 0
                n4_Mat_Hos = 0
                n3_Prex = 0            
                      
        
        
        else:
            Tot2 = 0
            n4_Amb = 0
            n4_Hos = 0
            n4_Mat_Amb = 0
            n4_Mat_Hos = 0
            n3_Prex = 0
         
        
        Egreso_Neto = max(Tot2, 0)    
        Distr_Pagos = np.append(Distr_Pagos, Egreso_Neto)   #Aqui guardamos el monto pagado para la aseguradora para la iteracion j
        Reclamos_Amb = np.append(Reclamos_Amb, n4_Amb)   #Aqui guardamos el numero de reclamos ambulatorios para la iteracion j
        Reclamos_Hos = np.append(Reclamos_Hos, n4_Hos)   #Aqui guardamos el numero de reclamos ambulatorios para la iteracion j
        Reclamos_Mat_Amb = np.append(Reclamos_Mat_Amb, n4_Mat_Amb)   #Aqui guardamos el numero de reclamos de maternidad ambulatorios para la iteracion j
        Reclamos_Mat_Hos = np.append(Reclamos_Mat_Hos, n4_Mat_Hos)   #Aqui guardamos el numero de reclamos de maternidad hospitalarios para la iteracion j
        Reclamos_Prex = np.append(Reclamos_Prex, n3_Prex)   #Aqui guardamos el numero de reclamos ambulatorios para la iteracion j
    
        if j % 5000 == 0:
            print("Iteracion número {0} de {1}".format(j+5000, my_iter))
        
    Distr_Pagos = np.sort(Distr_Pagos)
    k = int(np.floor(my_iter*(1-prob_perdida)))
    
    PPm = np.mean(Distr_Pagos)
    PPp = Distr_Pagos[k]  
    r_Amb = np.mean(Reclamos_Amb)
    r_Hos = np.mean(Reclamos_Hos)
    r_Mat_Amb = np.mean(Reclamos_Mat_Amb)
    r_Mat_Hos = np.mean(Reclamos_Mat_Hos)
    r_Prex = np.mean(Reclamos_Prex)   
    
    return (PPm, PPp, r_Amb, r_Hos, r_Mat_Amb, r_Mat_Hos, r_Prex)


    



 
 







    




