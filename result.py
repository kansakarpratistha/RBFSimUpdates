import streamlit as st
import time
import numpy as np
import pandas as pd
import sympy
import model_pro
from plot import *


def app():
    st.sidebar.divider()
    st.title(":red[Results and visualizations]")
    
    st.markdown("---")

    if 'aq_ls' and 'we_ls' and 'cf_ls' not in st.session_state:
        st.subheader(":blue[Please Input Data for the simulation]")
    if 'aq_ls' and 'we_ls' and 'cf_ls' in st.session_state :
        if len(st.session_state.aq_ls)==0 and len(st.session_state.we_ls) == 0 :
            st.subheader(":blue[Please Input required data for the simulation]")
        if len(st.session_state.aq_ls) and (st.session_state.we_ls) !=0 :
            results_aq = st.session_state.aq_ls
            results = st.session_state.we_ls
            results_clg = st.session_state.cf_ls

            aem_model = model_pro.Model(k=results_aq[0][4], H=results_aq[0][1], h0=results_aq[0][5], Qo_x=results_aq[0][2])
            #------------------------Check AEM Model
            if len(results_clg) == 0:
                st.info("No Clogging Factor is Added!")
            else:
                aem_model.calc_clogging(results_clg[0][1], results_clg[0][2])
            
            if len(results) == 0:
                st.error("Please add at least one Well")
            else:
                for j in range(6):
                    if j == len(results):
                        for i in range(j):
                            well = model_pro.Well(aem_model, Q=results[i][1], rw=0.2, x=results[i][2], y=results[i][3])
            
                c1, c2= st.columns(2)

                # ------------------------------------------------------------------Stream / Potential Lines for Multiple Wells-----------------------------    
                with c1:
                    if len(results)>(1):
                        st.subheader(":blue[Wells in Flow Field:]")
                    else:
                        st.subheader(":blue[Well in Flow Field:]")
                    plot1 = plotting(0, 100, -20, 150, 100)
                    b, fig1 = plot1.plot2d(aem_model, levels=8, sharey=False, quiver=False, streams=True, figsize=(18, 12))
                    st.pyplot(fig1)                        
                    
                                    
                # ------------------------------------------------------------------------------Download Files----------------------------------------------------------------------------------------
                plot3 = plotting(0, 100, -20, 150, 100)

                h0, psi0 = plot3.fix_to_mesh(aem_model)
                dfh = pd.DataFrame(data=h0)
                df_psi = pd.DataFrame(data=psi0)
                dfh_rounded = dfh.round(decimals=3)
                df_psi_rounded = df_psi.round(decimals=3)
                csv = dfh_rounded.to_csv(sep="\t", index=False)
                csv_psi = df_psi_rounded.to_csv(sep="\t", index=False)

                st.sidebar.markdown("---")
                st.sidebar.title("Download \u03C8 & Head:")
                st.sidebar.download_button(label="Download H in CSV", data=csv, mime="csv")
                st.sidebar.download_button(label="Download \u03C8 in CSV", data=csv_psi, mime="csv")

            st.sidebar.markdown("---")
