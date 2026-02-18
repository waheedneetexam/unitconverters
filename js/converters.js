/**
 * converters.js — All unit conversion logic
 * UnitConvert.net
 */

const CONVERTERS = {

  length: {
    name: 'Length',
    icon: '📏',
    baseUnit: 'meter',
    units: [
      { id: 'meter',       label: 'Meter (m)',              factor: 1 },
      { id: 'kilometer',   label: 'Kilometer (km)',          factor: 1000 },
      { id: 'centimeter',  label: 'Centimeter (cm)',         factor: 0.01 },
      { id: 'millimeter',  label: 'Millimeter (mm)',         factor: 0.001 },
      { id: 'micrometer',  label: 'Micrometer (µm)',         factor: 1e-6 },
      { id: 'nanometer',   label: 'Nanometer (nm)',          factor: 1e-9 },
      { id: 'mile',        label: 'Mile (mi)',               factor: 1609.344 },
      { id: 'yard',        label: 'Yard (yd)',               factor: 0.9144 },
      { id: 'foot',        label: 'Foot (ft)',               factor: 0.3048 },
      { id: 'inch',        label: 'Inch (in)',               factor: 0.0254 },
      { id: 'nautical',    label: 'Nautical Mile (nmi)',     factor: 1852 },
      { id: 'lightyear',   label: 'Light Year (ly)',         factor: 9.461e15 },
      { id: 'furlong',     label: 'Furlong',                 factor: 201.168 },
      { id: 'chain',       label: 'Chain',                   factor: 20.1168 },
    ],
    convert(value, from, to) {
      const fromUnit = this.units.find(u => u.id === from);
      const toUnit   = this.units.find(u => u.id === to);
      if (!fromUnit || !toUnit) return NaN;
      return value * fromUnit.factor / toUnit.factor;
    }
  },

  temperature: {
    name: 'Temperature',
    icon: '🌡️',
    units: [
      { id: 'celsius',    label: 'Celsius (°C)' },
      { id: 'fahrenheit', label: 'Fahrenheit (°F)' },
      { id: 'kelvin',     label: 'Kelvin (K)' },
      { id: 'rankine',    label: 'Rankine (°R)' },
      { id: 'reaumur',    label: 'Réaumur (°Ré)' },
    ],
    convert(value, from, to) {
      // Convert to Celsius first
      let celsius;
      switch (from) {
        case 'celsius':    celsius = value; break;
        case 'fahrenheit': celsius = (value - 32) * 5/9; break;
        case 'kelvin':     celsius = value - 273.15; break;
        case 'rankine':    celsius = (value - 491.67) * 5/9; break;
        case 'reaumur':    celsius = value * 5/4; break;
        default: return NaN;
      }
      // Convert from Celsius to target
      switch (to) {
        case 'celsius':    return celsius;
        case 'fahrenheit': return celsius * 9/5 + 32;
        case 'kelvin':     return celsius + 273.15;
        case 'rankine':    return (celsius + 273.15) * 9/5;
        case 'reaumur':    return celsius * 4/5;
        default: return NaN;
      }
    }
  },

  area: {
    name: 'Area',
    icon: '⬛',
    baseUnit: 'sqmeter',
    units: [
      { id: 'sqmeter',      label: 'Square Meter (m²)',       factor: 1 },
      { id: 'sqkilometer',  label: 'Square Kilometer (km²)',  factor: 1e6 },
      { id: 'sqcentimeter', label: 'Square Centimeter (cm²)', factor: 1e-4 },
      { id: 'sqmillimeter', label: 'Square Millimeter (mm²)', factor: 1e-6 },
      { id: 'sqmicrometer', label: 'Square Micrometer (µm²)', factor: 1e-12 },
      { id: 'hectare',      label: 'Hectare (ha)',            factor: 10000 },
      { id: 'sqmile',       label: 'Square Mile (mi²)',       factor: 2589988.11 },
      { id: 'sqyard',       label: 'Square Yard (yd²)',       factor: 0.836127 },
      { id: 'sqfoot',       label: 'Square Foot (ft²)',       factor: 0.092903 },
      { id: 'sqinch',       label: 'Square Inch (in²)',       factor: 0.00064516 },
      { id: 'acre',         label: 'Acre',                    factor: 4046.856 },
    ],
    convert(value, from, to) {
      const fromUnit = this.units.find(u => u.id === from);
      const toUnit   = this.units.find(u => u.id === to);
      if (!fromUnit || !toUnit) return NaN;
      return value * fromUnit.factor / toUnit.factor;
    }
  },

  volume: {
    name: 'Volume',
    icon: '🧊',
    baseUnit: 'liter',
    units: [
      { id: 'liter',       label: 'Liter (L)',               factor: 1 },
      { id: 'milliliter',  label: 'Milliliter (mL)',          factor: 0.001 },
      { id: 'cubicmeter',  label: 'Cubic Meter (m³)',         factor: 1000 },
      { id: 'cubicfoot',   label: 'Cubic Foot (ft³)',         factor: 28.3168 },
      { id: 'cubicinch',   label: 'Cubic Inch (in³)',         factor: 0.0163871 },
      { id: 'cubicyard',   label: 'Cubic Yard (yd³)',         factor: 764.555 },
      { id: 'usgallon',    label: 'US Gallon (gal)',          factor: 3.78541 },
      { id: 'ukgallon',    label: 'UK Gallon (gal)',          factor: 4.54609 },
      { id: 'usquart',     label: 'US Quart (qt)',            factor: 0.946353 },
      { id: 'uspint',      label: 'US Pint (pt)',             factor: 0.473176 },
      { id: 'uscup',       label: 'US Cup',                   factor: 0.236588 },
      { id: 'usfloz',      label: 'US Fluid Ounce (fl oz)',   factor: 0.0295735 },
      { id: 'tablespoon',  label: 'Tablespoon (tbsp)',        factor: 0.0147868 },
      { id: 'teaspoon',    label: 'Teaspoon (tsp)',           factor: 0.00492892 },
    ],
    convert(value, from, to) {
      const fromUnit = this.units.find(u => u.id === from);
      const toUnit   = this.units.find(u => u.id === to);
      if (!fromUnit || !toUnit) return NaN;
      return value * fromUnit.factor / toUnit.factor;
    }
  },

  weight: {
    name: 'Weight',
    icon: '⚖️',
    baseUnit: 'kilogram',
    units: [
      { id: 'kilogram',    label: 'Kilogram (kg)',            factor: 1 },
      { id: 'gram',        label: 'Gram (g)',                 factor: 0.001 },
      { id: 'milligram',   label: 'Milligram (mg)',           factor: 1e-6 },
      { id: 'microgram',   label: 'Microgram (µg)',           factor: 1e-9 },
      { id: 'tonne',       label: 'Metric Ton (t)',           factor: 1000 },
      { id: 'pound',       label: 'Pound (lb)',               factor: 0.453592 },
      { id: 'ounce',       label: 'Ounce (oz)',               factor: 0.0283495 },
      { id: 'stone',       label: 'Stone (st)',               factor: 6.35029 },
      { id: 'uston',       label: 'US Ton (short ton)',       factor: 907.185 },
      { id: 'ukton',       label: 'UK Ton (long ton)',        factor: 1016.05 },
      { id: 'carat',       label: 'Carat (ct)',               factor: 0.0002 },
    ],
    convert(value, from, to) {
      const fromUnit = this.units.find(u => u.id === from);
      const toUnit   = this.units.find(u => u.id === to);
      if (!fromUnit || !toUnit) return NaN;
      return value * fromUnit.factor / toUnit.factor;
    }
  },

  time: {
    name: 'Time',
    icon: '⏱️',
    baseUnit: 'second',
    units: [
      { id: 'second',      label: 'Second (s)',               factor: 1 },
      { id: 'millisecond', label: 'Millisecond (ms)',          factor: 0.001 },
      { id: 'microsecond', label: 'Microsecond (µs)',          factor: 1e-6 },
      { id: 'nanosecond',  label: 'Nanosecond (ns)',           factor: 1e-9 },
      { id: 'minute',      label: 'Minute (min)',              factor: 60 },
      { id: 'hour',        label: 'Hour (h)',                  factor: 3600 },
      { id: 'day',         label: 'Day (d)',                   factor: 86400 },
      { id: 'week',        label: 'Week (wk)',                 factor: 604800 },
      { id: 'month',       label: 'Month (avg)',               factor: 2629800 },
      { id: 'year',        label: 'Year (yr)',                 factor: 31557600 },
      { id: 'decade',      label: 'Decade',                   factor: 315576000 },
      { id: 'century',     label: 'Century',                  factor: 3155760000 },
    ],
    convert(value, from, to) {
      const fromUnit = this.units.find(u => u.id === from);
      const toUnit   = this.units.find(u => u.id === to);
      if (!fromUnit || !toUnit) return NaN;
      return value * fromUnit.factor / toUnit.factor;
    }
  },

  speed: {
    name: 'Speed',
    icon: '🚀',
    baseUnit: 'mps',
    units: [
      { id: 'mps',         label: 'Meter/Second (m/s)',       factor: 1 },
      { id: 'kph',         label: 'Kilometer/Hour (km/h)',    factor: 0.277778 },
      { id: 'mph',         label: 'Mile/Hour (mph)',          factor: 0.44704 },
      { id: 'fps',         label: 'Foot/Second (ft/s)',       factor: 0.3048 },
      { id: 'knot',        label: 'Knot (kn)',                factor: 0.514444 },
      { id: 'mach',        label: 'Mach (at sea level)',      factor: 340.29 },
      { id: 'lightspeed',  label: 'Speed of Light (c)',       factor: 299792458 },
    ],
    convert(value, from, to) {
      const fromUnit = this.units.find(u => u.id === from);
      const toUnit   = this.units.find(u => u.id === to);
      if (!fromUnit || !toUnit) return NaN;
      return value * fromUnit.factor / toUnit.factor;
    }
  },

  pressure: {
    name: 'Pressure',
    icon: '🔵',
    baseUnit: 'pascal',
    units: [
      { id: 'pascal',      label: 'Pascal (Pa)',              factor: 1 },
      { id: 'kilopascal',  label: 'Kilopascal (kPa)',         factor: 1000 },
      { id: 'megapascal',  label: 'Megapascal (MPa)',         factor: 1e6 },
      { id: 'bar',         label: 'Bar',                      factor: 100000 },
      { id: 'millibar',    label: 'Millibar (mbar)',          factor: 100 },
      { id: 'atm',         label: 'Atmosphere (atm)',         factor: 101325 },
      { id: 'psi',         label: 'PSI (lb/in²)',             factor: 6894.76 },
      { id: 'torr',        label: 'Torr (mmHg)',              factor: 133.322 },
      { id: 'mmhg',        label: 'Millimeter of Mercury',    factor: 133.322 },
      { id: 'inhg',        label: 'Inch of Mercury (inHg)',   factor: 3386.39 },
    ],
    convert(value, from, to) {
      const fromUnit = this.units.find(u => u.id === from);
      const toUnit   = this.units.find(u => u.id === to);
      if (!fromUnit || !toUnit) return NaN;
      return value * fromUnit.factor / toUnit.factor;
    }
  },

  energy: {
    name: 'Energy',
    icon: '⚡',
    baseUnit: 'joule',
    units: [
      { id: 'joule',       label: 'Joule (J)',                factor: 1 },
      { id: 'kilojoule',   label: 'Kilojoule (kJ)',           factor: 1000 },
      { id: 'megajoule',   label: 'Megajoule (MJ)',           factor: 1e6 },
      { id: 'calorie',     label: 'Calorie (cal)',            factor: 4.184 },
      { id: 'kilocalorie', label: 'Kilocalorie (kcal)',        factor: 4184 },
      { id: 'wh',          label: 'Watt-Hour (Wh)',           factor: 3600 },
      { id: 'kwh',         label: 'Kilowatt-Hour (kWh)',      factor: 3600000 },
      { id: 'mwh',         label: 'Megawatt-Hour (MWh)',      factor: 3.6e9 },
      { id: 'btu',         label: 'BTU (British Thermal)',    factor: 1055.06 },
      { id: 'therm',       label: 'Therm (US)',               factor: 1.055e8 },
      { id: 'ev',          label: 'Electronvolt (eV)',        factor: 1.602e-19 },
      { id: 'ftlb',        label: 'Foot-Pound (ft·lb)',       factor: 1.35582 },
    ],
    convert(value, from, to) {
      const fromUnit = this.units.find(u => u.id === from);
      const toUnit   = this.units.find(u => u.id === to);
      if (!fromUnit || !toUnit) return NaN;
      return value * fromUnit.factor / toUnit.factor;
    }
  },
};

// ── Helper: format number nicely ──
function formatResult(num) {
  if (isNaN(num) || !isFinite(num)) return '—';
  if (num === 0) return '0';
  const abs = Math.abs(num);
  if (abs >= 1e15 || (abs < 1e-6 && abs > 0)) {
    return num.toExponential(6);
  }
  if (abs >= 1000) {
    return num.toLocaleString('en-US', { maximumFractionDigits: 6 });
  }
  return parseFloat(num.toPrecision(10)).toString();
}

// ── Export for use in app.js ──
window.CONVERTERS = CONVERTERS;
window.formatResult = formatResult;
