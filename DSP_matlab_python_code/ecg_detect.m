function ecg_detect(input_file)
    fs = 360;
    duration = 10;
    N = fs * duration;

    data = readmatrix(input_file);
    ecg = data(2:N+1, 3);  

    Y = fft(ecg);
    f = (0:N-1) * (fs/N);
    Y_mag = abs(Y)/N;

    f_half = f(1:floor(N/2));
    Y_half = Y_mag(1:floor(N/2));
    a=length(f_half);
    b=length(Y_half);

    bw_energy = mean(Y_half(f_half >= 0.1 & f_half <= 0.5));
    baseline_detected = bw_energy > 0.01;

    pw_band = (f_half >= 50 & f_half <= 60);
    powerline_peak = max(Y_half(pw_band));
    powerline_mean=mean(Y_half(pw_band));
    powerline_detected = powerline_peak > 2.5*powerline_mean;

    headers = {'baseline_detected', 'powerline_detected'};
    writecell(headers, 'results.csv');
    writematrix([baseline_detected, powerline_detected], 'results.csv', 'WriteMode', 'append');

    spectrum = [f_half(:), Y_half(:)];
    writematrix(spectrum, 'spectrum.csv');
end
