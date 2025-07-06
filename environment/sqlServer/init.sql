-- Create the Instrument table
CREATE TABLE Instruments (
    instrumentID SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    audioCount INT
);

-- Create the AudioFiles table
CREATE TABLE AudioFiles (
    audioID SERIAL PRIMARY KEY,
    filePath VARCHAR(100) NOT NULL,
    sampleRate INT,
    duration INT,
    instrumentID INT,
    FOREIGN KEY (instrumentID) REFERENCES Instruments(instrumentID)
);

-- Create the FeatureTypes table to define different image generation methods
CREATE TABLE FeatureTypes (
    featureTypeID SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    description TEXT,
    parameters JSONB -- Store method-specific parameters
);

-- Create the Processed table with support for multiple feature types
CREATE TABLE Processed (
    processedID SERIAL PRIMARY KEY,
    instrumentID INT,
    audioID INT,
    fixedLength INT,
    featureTypeID INT,
    featurePath VARCHAR(200), -- Path to the generated feature file
    augmentation VARCHAR(50) CHECK (augmentation IN ('original', 'time_stretch', 'pitch_shifting', 'noise')),
    FOREIGN KEY (instrumentID) REFERENCES Instruments(instrumentID),
    FOREIGN KEY (audioID) REFERENCES AudioFiles(audioID),
    FOREIGN KEY (featureTypeID) REFERENCES FeatureTypes(featureTypeID)
);

-- Insert default feature types
INSERT INTO FeatureTypes (name, description, parameters) VALUES
('mel_spectrogram', 'Mel-frequency spectrogram', '{"n_mels": 128, "fmin": 0, "fmax": null}'),
('mfcc', 'Mel-frequency cepstral coefficients', '{"n_mfcc": 13, "n_mels": 128}'),
('chromagram', 'Chroma features', '{"n_chroma": 12}'),
('spectral_contrast', 'Spectral contrast features', '{"n_bands": 6}'),
('tonnetz', 'Tonal centroid features', '{}'),
('constant_q', 'Constant-Q transform', '{"bins_per_octave": 12, "n_bins": 84}'),
('cqt', 'Constant-Q chromagram', '{"bins_per_octave": 12, "n_bins": 84}'),
('stft', 'Short-time Fourier transform', '{"n_fft": 2048, "hop_length": 512}'),
('harmonic_percussive', 'Harmonic-percussive source separation', '{"margin": 3.0}'),
('onset_strength', 'Onset strength envelope', '{"hop_length": 512}');