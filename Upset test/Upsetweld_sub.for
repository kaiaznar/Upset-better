C 
C Fortran code for UAMP and FRIC subroutines for Upsetweld simulation
C
      SUBROUTINE UAMP(
     *     ampName, time, ampValueOld, dt, nProps, props, nSvars, 
     *     svars, lFlagsInfo,
     *     nSensor, sensorValues, sensorNames, jSensorLookUpTable, 
     *     AmpValueNew, 
     *     lFlagsDefine,
     *     AmpDerivative, AmpSecDerivative, AmpIncIntegral,
     *     AmpDoubleIntegral)
C
      INCLUDE 'ABA_PARAM.INC'
      COMMON/SPIN/SFORCE,SPINRATE
C   !,KFLAG
C     time indices
      parameter (iStepTime        = 1,
     *           iTotalTime       = 2,
     *           nTime            = 2)
C     flags passed in for information
      parameter (iInitialization   = 1,
     *           iRegularInc       = 2,
     *           iCuts             = 3,
     *           ikStep            = 4,
     *           nFlagsInfo        = 4)
C     optional flags to be defined
      parameter (iComputeDeriv       = 1,
     *           iComputeSecDeriv    = 2,
     *           iComputeInteg       = 3,
     *           iComputeDoubleInteg = 4,
     *           iStopAnalysis       = 5,
     *           iConcludeStep       = 6,
     *           nFlagsDefine        = 6)
      dimension time(nTime), lFlagsInfo(nFlagsInfo),
     *          lFlagsDefine(nFlagsDefine)
      dimension jSensorLookUpTable(*)
      dimension sensorValues(nSensor), svars(nSvars), props(nProps)
      character*80 sensorNames(nSensor)
      character*80 ampName
C
      PARAMETER(omega=52.36D0)
      integer i, n, KFLAG
      real LUPSET, nT, dF, dU, PiC, lastForce, lastUpset, lastSpinR
      real thisUpset, spinTest
      real, dimension(9) :: cT, cF, cU
      sTime = time(iStepTime)
      cTime=props(1)+sTime+57.0
      tTime = time(iTotalTime)
      iDisp=5D0
      weldStepTime=0.01
      PiC=3.14159265359
      lastForce=props(2)
      lastUpset=props(3)
      lastSpinR=props(4)
      write (7,*)  'LF LU LS= ', lastForce, lastUpset, lastSpinR
C
C ----sensor----------------------------------------------------------
      UPSET = GetSensorValue('UPSET',
     *                             jSensorLookUpTable,
     *                             sensorValues)
         if (lFlagsInfo(ikStep).EQ.2) then
           write (7,*)  'upset= ', -(UPSET+iDisp)+lastUpset
         else if(lFlagsInfo(ikStep).EQ.3) then
           write (7,*)  'upset= ', -(UPSET+iDisp)+lastUpset

         else
         end if
      FORCE = GetSensorValue('FORCE',
     *                             jSensorLookUpTable,
     *                             sensorValues)
         if (lFlagsInfo(ikStep).EQ.2) then
           write (7,*)  'force= ', -FORCE
         else
         end if

C ----amplitude values-----------------------------------------------
C
      spinTest = lastSpinR-omega/2.2*tTime
        if(ampName.eq.'ROT_AMP') then
          if(lastUpset.LE.20.0) then
            ampValueNew = omega
          else
            if(spinTest.LE.5.0) then
              ampValueNew = 0.0
            else
              ampValueNew = spinTest
            end if
          end if
          SPINRATE = ampValueNew
        else if(ampName.eq.'DISP_AMP') then
          if(lastUpset.LE.1.0) then
            ampValueNew = 0.05
          else
            ampValueNew = 0.0
          end if
        else if(ampName.eq.'FORCE_AMP') then
          if(lastUpset.LE.20.0) then
            ampValueNew=lastForce+sTime*4500.0
          else
            ampValueNew=lastForce
          end if
        else
        end if

         write (7,*)  'spinR= ', SPINRATE
      RETURN
      END
C
C ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
C
C     USER FRICTION SUBROUTINE
C     
      SUBROUTINE FRIC(LM,TAU,DDTDDG,DDTDDP,DSLIP,SED,SFD,
     1     DDTDDT,PNEWDT,STATEV,DGAM,TAULM,PRESS,DPRESS,DDPDDH,SLIP,
     2     KSTEP,KINC,TIME,DTIME,NOEL,CINAME,SLNAME,MSNAME,NPT,NODE,
     3     NPATCH,COORDS,RCOORD,DROT,TEMP,PREDEF,NFDIR,MCRD,NPRED,
     4     NSTATV,CHRLNGTH,PROPS,NPROPS)
C     
      INCLUDE 'ABA_PARAM.INC'
      COMMON/SPIN/SFORCE,SPINRATE
C     
      CHARACTER*80 CINAME,SLNAME,MSNAME
      CHARACTER*80 CPNAME
      DIMENSION TAU(NFDIR),DDTDDG(NFDIR,NFDIR),DDTDDP(NFDIR),
     1     DSLIP(NFDIR),DDTDDT(NFDIR,2),STATEV(*),
     2     DGAM(NFDIR),TAULM(NFDIR),SLIP(NFDIR),TIME(2),
     3     COORDS(MCRD),RCOORD(MCRD),DROT(2,2),TEMP(2),
     4     PREDEF(2,*),PROPS(NPROPS)
C     
      PARAMETER (SCALE=1.D3)
      LOGICAL LOCAL,CONSTANT,DOUBLEMASTER,FLYWHEELRATE,LDEBUG
      PARAMETER (LOCAL        = .FALSE. )
      PARAMETER (DOUBLEMASTER = .TRUE. )
      PARAMETER (CONSTANT     = .true. )
      PARAMETER (FLYWHEELRATE = .TRUE. )
      PARAMETER (LDEBUG       = .false. )
      PARAMETER(ZERO=0.0D0,ONE=1.0D0,TWO=2.0D0)
C     
C     FRICTION MODEL PARAMETERS
C     
      PARAMETER(omega=52.36D0)
C     CONSTANT-COEFFICIENT VALUE
      PARAMETER(CFRIC=0.3D0)
C     CONSTANT-COEFFICIENT TRANSITION SLIP RATE
      PARAMETER(CTRANS=1.0D-2)
C     CONSTANT CONTACT AREA
      PARAMETER(AREA=1859.705D0)
      cTime=props(1)+TIME(1)+57.0
C     
      IF (LDEBUG) THEN
         write (7,*)  'Weld pressure = ',SFORCE, SPINRATE
      END IF

        APRESS = PRESS

C
      LOCNUM = 0
      JRCD   = 0
      JTYP   = 0
      CALL GETPARTINFO(NODE, JTYP, CPNAME, LOCNUM, JRCD)
C
C
      IF (LM .EQ. 2) RETURN
C     
C-----Material Propertie Shear yield
      if(TEMP(1).GT.TEMP(2)) then
        SOL = TEMP(1)
      else
        SOL = TEMP(2)
      end if
C
      if(SOL.GT.1350.0) then
        SOL = 1350.0
      else
      end if
C

      roomShear=346.41
C
      if(SOL.LE.1000.0) then

        tauY=roomShear*(-9.8980E-04*SOL + 1.0198E+00)
        dTauY=roomShear*(-9.8980E-04)
      else if((SOL.LE.1350.0).and.(SOL.GT.1000.0)) then
       tauY=roomShear*(-8.5714E-05*SOL + 1.1571E-01)
       dTauY=roomShear*(-8.5714E-05)
      else
       tauY=0.0
       dTauY=0.0
      end if
C

      SDIR = SIGN(ONE,DGAM(2))



      SRATE = ABS(DGAM(2)/DTIME)
      SRATEM = SRATE/SCALE
C

      if(KINC.LE.1) then
        LM=2
      else
        LM=0
      end if
C

C     
      IF ((DSLIP(2)*DGAM(2)).lt.0.0) THEN
         write (7,*) '*** WARNING.  SLIP REVERSAL AT NODE ',LOCNUM
         write (7,*) '                      PART INSTANCE ',CPNAME
         IF (FLYWHEELRATE) THEN
            write (7,*) '       FLYWHEEL-PREDICTED SLIP RATE ',
     $           -SRATE*SDIR
            write (7,*) '                           MEASURED ',
     $           DGAM(2)/DTIME
         END IF
         write (7,*) ' '
      END IF
C
C        CONSTANT FRICTION COEFFICIENT
C        
         IF (SRATEM.GT.CTRANS) THEN
            TAU(1)=ZERO
            TAU(2)=CFRIC*APRESS
C
            if(abs(TAU(2)).GT.tauY) then
              TAU(2)=TauY

              DDTDDP(1)=ZERO
              DDTDDP(2)=ZERO
            else

              DDTDDP(1)=ZERO
              DDTDDP(2)=CFRIC
            end if
C           
            DDTDDG(1,1)=ZERO
            DDTDDG(2,2)=ZERO
            DDTDDG(1,2)=ZERO
            DDTDDG(2,1)=ZERO
         ELSE
            TAU(1)=ZERO
            TAU(2)=CFRIC*APRESS * (SRATEM/CTRANS)
C
            if(abs(TAU(2)).GT.tauY) then
              TAU(2)=TauY

              DDTDDP(1)=ZERO
              DDTDDP(2)=ZERO
            else

              DDTDDP(1)=ZERO
              DDTDDP(2)=CFRIC*(SRATEM/CTRANS)
            end if
C
            DDTDDG(1,1)=ZERO
            DDTDDG(2,2)=CFRIC * ((APRESS/DTIME) /CTRANS) / SCALE
            DDTDDG(1,2)=ZERO
            DDTDDG(2,1)=ZERO
         END IF
C     

         DSLIP(1)=DGAM(1)
         DSLIP(2)=SRATE*DTIME

C     
C     SET SIGN OF ROTATION-DIRECTION SHEAR TERMS
C     
      TAU(2)      = SDIR * abs(TAU(2))
      DDTDDP(2)   = SDIR * DDTDDP(2)
      IF (LDEBUG) THEN
         write (7,*)  'FRIC: KINC = ',KINC
         write (7,*)  'NODE  = ',LOCNUM
         write (7,*)  'INSTANCE  = ',CPNAME
         write (7,*)  'SRATE = ',SRATEM
         write (7,*)  'TAU   = ',TAU(2)
         write (7,*)  'SDIR  = ',SDIR
         write (7,*)  'COEFF = ',DDTDDP(2)
         write (7,*)  'PRESSURE = ',APRESS
         write (7,*)  'DDTDDG = ',DDTDDG(2,2)
         write (7,*)  ' '
      END IF
C
      SFD = abs(TAU(2)*SRATE)
C     
      RETURN
      END