#include <ti/screen.h>
#include <ti/getcsc.h>
#include <ti/getkey.h>
#include <sys/timers.h>
#include <ti/real.h>
#include <time.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdio.h>

#define FLAG_LEN 18
#define SLEEP_TIME 10
#define ROUND_PREC 9
#define WAIT_FOR_KEY() while (!os_GetCSC());

// i'm feeling nice to we keep the symbols for these

cplx_t __attribute__ ((noinline)) os_CplxMul(cplx_t a, cplx_t b)
{
    cplx_t res;
    real_t tmp1 = os_RealMul(&a.real, &b.real);
    real_t tmp2 = os_RealMul(&a.imag, &b.imag);
    real_t tmp3 = os_RealMul(&a.real, &b.imag);
    real_t tmp4 = os_RealMul(&a.imag, &b.real);
    res.real = os_RealSub(&tmp1, &tmp2);
    res.imag = os_RealAdd(&tmp3, &tmp4);
    return res;
}

cplx_t __attribute__ ((noinline)) os_CplxAdd(cplx_t a, cplx_t b)
{
    cplx_t res;
    res.real = os_RealAdd(&a.real, &b.real);
    res.imag = os_RealAdd(&a.imag, &b.imag);
    return res;
}

bool __attribute__ ((noinline)) os_CplxEqual(cplx_t a, cplx_t b)
{
    real_t diff_real = os_RealSub(&a.real, &b.real);
    real_t diff_imag = os_RealSub(&a.imag, &b.imag);
    real_t zero = os_Int24ToReal(0);
    diff_real = os_RealRound(&diff_real, ROUND_PREC);
    diff_imag = os_RealRound(&diff_imag, ROUND_PREC);
    return os_RealCompare(&diff_real, &zero) == 0 && os_RealCompare(&diff_imag, &zero) == 0;
}

// these symbols end up in the map so we keep them a little ambiguous instead of "matrix" and "vec" or smth
char *m[] = {"-0.341984671631458","0.404391666886198","0.859751816831620","0.215383753378763","-0.582345047944453","0.300404641573834","-0.297281686342036","0.0189958589519295","0.745337682399741","-0.926863873345966","0.285063710805262","-0.449063311054464","-0.980862417807265","-0.472018368371501","0.197362363730076","0.627219335823120","-0.284057956944491","0.469168607416927","-0.713997356570543","-0.753301437928382","0.815723107505558","0.315045529470803","-0.0800719053376702","0.526503466439483","0.492426416346098","-0.615857024040712","-0.741773074055450","0.425700773972636","0.368965517352886","0.821335596606472","0.189731156841746","-0.807635502485287","-0.800362171389760","0.532288136986850","-0.852182106777362","-0.443958826977312","-0.915986060298440","0.706173539423122","0.316330078883681","-0.204561892388161","-0.214164316596168","0.668977677309302","0.897165181570476","0.107903328188376","-0.612080687447771","-0.307529136915603","0.249591112039302","0.574723332087470","0.868886360330553","-0.356482734156603","-0.552100213430986","0.706031729420971","-0.324417044299569","0.414874753136943","-0.649124587428091","0.792654663549957","0.450616434005459","-0.0582589749352991","-0.254201166781082","0.222540311223398","-0.358106100040021","0.597546234550927","0.261341184452891","0.436864004201145","-0.382970489581628","0.782020231153203","0.539663645066043","-0.748419927983316","-0.677046608399105","0.765804323912875","0.780303158890230","0.550434733542643","0.848146281912411","0.854095885067771","0.116408293517155","0.377612195420903","-0.948982251453998","0.587230032007002","-0.578853740181236","-0.189355531645957","0.0128225588600155","0.688652846047321","0.999557605838961","-0.671291998671785","-0.981041913213424","0.0416212205878765","0.512320101799739","0.0197660480206714","0.0620391978086416","0.681080211262800","-0.427258839313446","0.143358111960010","0.458845437064735","-0.576995384776285","0.552800455717514","0.291638234278100","-0.230805253874776","0.770931354349970","0.477729985730853","0.685982631138108","0.924189971048216","0.267854740380158","0.704561817231873","-0.113573055702265","-0.337549621668142","0.0919063111515570","0.258288009483394","-0.673879457428291","0.0914201191006181","-0.379658592170198","-0.694042807772379","-0.0508570575353127","0.228837520823041","0.601913024829833","-0.237785505981595","-0.726720770666128","-0.309888835804351","0.631728161916106","0.659946275395894","0.145677278833203","-0.196479398000753","-0.278555522931786","0.555973948393210","-0.642250352981302","0.666757608655483","-0.512061970740510","-0.668368690620697","0.151371566650451","0.173686574490933","0.849733761286468","-0.719746773981918","0.370649338756589","0.606789311445479","-0.958369965752596","0.311195951891349","-0.916568051191397","-0.648900474933963","0.903483765508038","-0.112289062980063","-0.0737614463141654","-0.00594001217267004","-0.554832148650263","-0.333638653132005","-0.442136974445374","-0.486025156316764","0.440316214160655","0.388624816109809","0.466603402778736","-0.497291534787145","0.592189077201445","0.725980975583035","-0.591189360552703","0.722471200526173","0.467607295911807","-0.572541166380293","0.229593682332073","0.352157028734345","-0.732188425967022","0.922274052349024","-0.735389739743189","-0.280664307656757","0.501733464715790"};
char *v[] = {"-12.1215595893463","-45.7620439722924","-57.8612785526394","-71.8644791050517","-178.222485685709","164.900849505901","-258.348959780483","225.030096815323","-170.166365073200","170.851434079567","110.886862042977","252.867710764252","136.470708962761","-21.3014295041732","-32.2563875398594","-139.348506754610","69.2658570030097","157.722920763045"};

void os_MoveCursor(int drow, int dcol)
{
    unsigned int curRow, curCol;
    os_GetCursorPos(&curRow, &curCol);
    os_SetCursorPos((unsigned int)((int)curRow + drow), (unsigned int)((int)curCol + dcol));
}

int main(void)
{
    char inp_buf[FLAG_LEN] = {0};

    os_ClrHome();

    os_EnableCursor();
    os_PutStrFull("Enter the password to decrypt your calculator:");
    os_NewLine();
    os_PutStrFull("SNHT{ }");
    os_MoveCursor(0, -2);

    char out_ch[] = {0, 0};
    for (int i = 0; i < FLAG_LEN; i++) {
        int key;
        while (key = os_GetKey(), key < k_CapA || key > k_CapZ) {
            if (key == k_Clear || key == k_Enter || key == k_Quit)
                return 0;
        }
        inp_buf[i] = out_ch[0] = 'A' + key - k_CapA;
        os_PutStrFull(out_ch);
        os_PutStrFull(" }");
        os_MoveCursor(0, -2);
    }
    os_DisableCursor();
    os_PutStrFull("} ");

    os_NewLine();
    os_NewLine();
    os_PutStrFull("Doing real shit...");
    os_NewLine();

    // i'm thinking this will give ppl time to break and see where the code is executing in the emulator
    clock_t start = clock();
    while (clock() - start < CLOCKS_PER_SEC * SLEEP_TIME);

    char out_str[0x20] = {0};

    for (int r = 0; r < FLAG_LEN/2; r++) {
        cplx_t sum = {0};
        cplx_t a = {0};
        cplx_t b = {0};
        for (int i = 0; i < FLAG_LEN/2; i++) {
            a.real = os_StrToReal(m[r*FLAG_LEN + 2*i], NULL);
            a.imag = os_StrToReal(m[r*FLAG_LEN + 2*i + 1], NULL);
            b.real = os_Int24ToReal(inp_buf[2*i]);
            b.imag = os_Int24ToReal(inp_buf[2*i+1]);
            sum = os_CplxAdd(sum, os_CplxMul(a, b));
        }
        cplx_t tgt_cplx = {0};
        tgt_cplx.real = os_StrToReal(v[2*r], NULL);
        tgt_cplx.imag = os_StrToReal(v[2*r + 1], NULL);
        if (!os_CplxEqual(sum, tgt_cplx)) {
            os_PutStrFull("Wrong! Please send BTC to me and I might give you the password.");
            WAIT_FOR_KEY();
            return 0;
        }
    }

    os_PutStrFull("What? How did you know?!");
    WAIT_FOR_KEY();

    return 0;
}