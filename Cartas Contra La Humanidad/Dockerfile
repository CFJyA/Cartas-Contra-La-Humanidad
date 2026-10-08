# Multi-stage build for ASP.NET Core 10 / 9 / 8
FROM mcr.microsoft.com/dotnet/sdk:9.0 AS build
WORKDIR /src

# Copy csproj and restore dependencies
COPY ["Cartas Contra La Humanidad.csproj", "./"]
RUN dotnet restore "Cartas Contra La Humanidad.csproj"

# Copy everything else and build release
COPY . .
RUN dotnet publish "Cartas Contra La Humanidad.csproj" -c Release -o /app/publish /p:UseAppHost=false

# Runtime stage
FROM mcr.microsoft.com/dotnet/aspnet:9.0 AS final
WORKDIR /app
EXPOSE 8080
ENV ASPNETCORE_URLS=http://+:8080
ENV ASPNETCORE_ENVIRONMENT=Production

COPY --from=build /app/publish .
ENTRYPOINT ["dotnet", "Cartas Contra La Humanidad.dll"]
