!!!!!!!!!!!!!!!!!!!!!!!!!!!   Program 5.1   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!                                                                       !
! Please Note:                                                          !
!                                                                       !
! (1) This computer program is written by Tao Pang in conjunction with  !
!     his book, "An Introduction to Computational Physics," published   !
!     by Cambridge University Press in 1997.                            !
!                                                                       !
! (2) No warranties, express or implied, are made for this program.     !
!                                                                       !
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!
!
SUBROUTINE DFT (FR,FI,GR,GI,N)
!
! Subroutine to perform the discrete Fourier transform with
! FR and FI as the real and imaginary parts of the input and
! GR and GI as the corresponding  output.
!
!f2py intent(in) n
!f2py intent(in) fr
!f2py intent(in) fi
!f2py intent(out) gr
!f2py intent(out) gi
!f2py depend(n) gr
!f2py depend(n) gi
  IMPLICIT NONE
  INTEGER, INTENT (IN) :: N
  INTEGER :: I,J
  REAL :: PI,X,Q
  REAL, INTENT (IN), DIMENSION (N) :: FR,FI
  REAL, INTENT (OUT), DIMENSION (N) :: GR,GI
!
  PI = 4.0*ATAN(1.0)
  X  = 2*PI/N
!
  DO I = 1, N
    GR(I) = 0.0
    GI(I) = 0.0
    DO J = 1, N
      Q = X*(J-1)*(I-1)
      GR(I) = GR(I)+FR(J)*COS(Q)+FI(J)*SIN(Q)
      GI(I) = GI(I)+FI(J)*COS(Q)-FR(J)*SIN(Q)
    END DO
  END DO
END SUBROUTINE DFT
