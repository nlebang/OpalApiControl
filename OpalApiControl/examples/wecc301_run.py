from run import run_model
import logging

logging.basicConfig(level=logging.DEBUG)


if __name__ == "__main__":
    localhost = 'tcp://127.0.0.1:5678'
    cui_aw = 'tcp://10.129.132.192:9999'
    cui = 'tcp://160.36.59.189:5000'
    kirsten = 'tcp://160.36.56.211:9898'
    ehsan = 'tcp://10.129.132.192:8801'
    run_model(project='WECC_DBW_RealTime', model='Real_Time', raw='WECC_10%Wind_PSSE_RAWCoords.raw', dyr='WECC_10%Wind_PSSE_DYR.dyr',
              path='C:/RT-LABv11_Workspace_New/', server=localhost)
