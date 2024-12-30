hist.Draw()

# Optionally, extend the x-axis to include the underflow bin (bin 0)
hist.GetXaxis().SetRange(0, hist.GetNbinsX() + 1)  # Display underflow and overflow bins

# Update and display the canvas
canvas.Update()
canvas.Draw()
