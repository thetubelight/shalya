#include "dac_output.hpp"
#include "control_state.hpp"

#include <Arduino.h>
#include <Wire.h>
#include <Adafruit_MCP4728.h>

constexpr uint8_t SDA_PIN = 21;
constexpr uint8_t SCL_PIN = 22;

constexpr auto ROLL_CHANNEL     = MCP4728_CHANNEL_A;
constexpr auto PITCH_CHANNEL    = MCP4728_CHANNEL_B;
constexpr auto THROTTLE_CHANNEL = MCP4728_CHANNEL_C;
constexpr auto YAW_CHANNEL      = MCP4728_CHANNEL_D;

//----------------------------------------------------
// Hardware configuration
//----------------------------------------------------

//while debugging the remote control(due to problems in flight), i found that throttle and pitch potentiometer are aligned in opposite directions relative to my design(i.e. at top : 0v, centre: 1.585v, down: 3.245v)

constexpr bool INVERT_ROLL       = false;
constexpr bool INVERT_PITCH      = true;
constexpr bool INVERT_THROTTLE   = true;
constexpr bool INVERT_YAW        = false;

constexpr uint16_t DAC_MIN    = 0;
constexpr uint16_t DAC_MAX    = 4095;
//we'll later add dac_centre and update these 3 variables acc to each potentiometer during caliberation

Adafruit_MCP4728 dac; //adafruit mcp4728 object, official demo code on github for this library uses mpc as object name, we are using dac


//----------------------------------------------------
// Convert [-1,1] -> [0,4095]
//----------------------------------------------------

static uint16_t mapAxis(float value)
{
    value = constrain(value, -1.0f, 1.0f);

    return (uint16_t)((value + 1.0f) * (DAC_MAX / 2.0f));
}


//----------------------------------------------------
// Apply hardware inversion if required
//----------------------------------------------------

static uint16_t applyAxisDirection(uint16_t value, bool invert)
{
    if (invert)
    {
        return DAC_MAX - value;
    }

    return value;
}


//----------------------------------------------------
// Init
//----------------------------------------------------

void initDAC()
{
    Wire.begin(SDA_PIN, SCL_PIN);

    if (!dac.begin())
    {
        Serial.println("MCP4728 not detected!");

        while (true)
        {
            delay(1000);
        }
    }

    Serial.println("MCP4728 Ready");
}


//----------------------------------------------------
// Update Outputs
//----------------------------------------------------

void updateDAC(const ControlState& state)
{
    dac.setChannelValue(
        ROLL_CHANNEL,
        applyAxisDirection(mapAxis(state.roll), INVERT_ROLL));

    dac.setChannelValue(
        PITCH_CHANNEL,
        applyAxisDirection(mapAxis(state.pitch), INVERT_PITCH));

    dac.setChannelValue(
        THROTTLE_CHANNEL,
        applyAxisDirection(mapAxis(state.throttle), INVERT_THROTTLE));

    dac.setChannelValue(
        YAW_CHANNEL,
        applyAxisDirection(mapAxis(state.yaw), INVERT_YAW));
}